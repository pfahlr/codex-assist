from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .utils import die
from .config import find_config_path, load_config, merge_config_into_args
from .context_ops import (
  apply_set_pairs, apply_set_file, apply_set_json, apply_set_json_file,
  apply_add, apply_add_file, apply_set_index, apply_set_file_index
)
from .structload import load_structured_glob
from .template_env import render_template


EXTENDED_HELP = r"""
Codex Template Builder - Extended Help
======================================

Overview
--------
Render Jinja2 templates using values from CLI flags and/or JSON/YAML config files.
Supports arrays, nested keys, file/glob inputs, and in-template includes.

Typical usage:
  python codex_template_builder.py \
    --template-name templates/prompt.tpl \
    --load config/base.yaml \
    --set owner=pfahlr --add tasks='Write tests' \
    --out out.txt

CLI flags (summary)
-------------------
--template-name PATH
--template-search DIR            # add lookup paths for {% include %} and helpers

--load PATH_OR_GLOB              # parse .json/.yaml/.yml; deep-merge mapping docs into root
--load-into KEY=PATH_OR_GLOB     # assign parsed doc(s) to KEY (scalar if one; list if many)

--set KEY=VALUE                  # scalar; VALUE may be '@file' (use @@ to escape '@')
--set-json KEY='<json>'
--set-json-file KEY=path.json

--set-file KEY='path/or/glob'    # 1 match -> scalar; many -> list (file contents)
--add KEY=VALUE                  # append scalar (or '@file') to list
--add-file KEY='glob/*.txt'      # append matched file contents to list
--set-index KEY:2=VALUE          # set list element (VALUE may be '@file')
--set-file-index KEY:2=path.txt  # set list element from a single file

--print-context                  # print final JSON context to stderr
--out PATH                       # write render to file (stdout if omitted)

--help-extended                  # show this extended help and exit

Configuration file format (JSON/YAML)
-------------------------------------
You can load structured config via:
  --load config/app.yaml
  --load-into DATA=inputs/*.json

Accepted document types:
  * Mapping (object/dict)  - recommended for --load (deep-merged into root)
  * Any JSON/YAML type     - allowed for --load-into (assigned to KEY)
  * Multi-document YAML    - each doc is loaded; see rules below

Merging rules:
  * --load: Each mapping document is deep-merged into the root context.
            Later files override earlier keys; nested dicts are merged.
  * --load-into KEY=...:
      - 1 file/doc -> KEY is that single value
      - many files/docs -> KEY is a list of those values (in lexicographic order)

Text tokens in config (scalar vs array)
---------------------------------------
As plain JSON/YAML, you can provide scalars, lists, and nested dicts:

YAML:
  owner: pfahlr
  tasks:
    - "Write tests"
    - "Fix CI"
  meta:
    repo: ragx
    branch: main

JSON:
  { "owner": "pfahlr", "tasks": ["Write tests", "Fix CI"], "meta": { "repo": "ragx" } }

File tokens in config (scalar vs array)
---------------------------------------
Use the following macros inside JSON/YAML to inline file contents:

  {"$file": "path/to/file.txt"}
      -> Replaced with the UTF-8 text of that file (scalar string)

  {"$files": ["a.txt", "b.txt"]}
      -> Replaced with a list of file texts (array of strings)

  {"$glob": "snips/*.md"}
      -> Replaced with a list of texts for all matching files (sorted lexicographically)

  {"$glob_one": "docs/intro.md"}
      -> Replaced with a single string; errors unless exactly one file matches

Optional:
  {"$glob": "snips/*.md", "$join": "\\n\\n---\\n\\n"}
      -> Joins all matched file texts with the given separator (produces a scalar string)

Examples:
  YAML (scalar file token):
    intro: { $file: docs/intro.md }

  YAML (array of files):
    snippets: { $glob: "snips/*.md" }

  YAML (joined into one big string):
    body: { $glob: "sections/*.md", $join: "\\n\\n" }

  YAML (explicit list of files):
    notes: { $files: ["n1.txt", "n2.txt"] }

Notes:
  * Paths support ~ and $VARS; globs are sorted lexicographically.
  * For --load (root merge), the resolved document must be a mapping (dict).
    If your top-level is a list or scalar, use --load-into KEY=...

Templates - includes & helpers
------------------------------
Native includes:
  {% include "partials/header.tpl" %}

Helpers (available as template globals):
  {{ include_text("docs/intro.md") }}
  {{ include_text_glob("snips/*.md", sep="\\n\\n") }}
  {% for p in glob_paths("snips/*.md") %}{{ include_text(p) }}{% endfor %}
  {{ read_json("data/spec.json").title }}

Tips
----
* Quote globs in the shell ('snips/*.md') for determinism and clear errors.
* Autoescape is OFF (rendering plain text). Escape as needed for HTML.
"""


def build_argparser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(
    description="Render a Jinja2 template with values from CLI flags (modular Codex Assistant).",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Tip: run with --help-extended for configuration schema and examples."
  )
  p.add_argument("--template-name", required=True, help="Path to the Jinja2 template file.")
  p.add_argument("--template-search", action="append", default=[], help="Additional template/include search paths. Repeatable.")
  p.add_argument("--config", help="Optional path to codex config (YAML/JSON). If omitted, default locations are searched.")
  p.add_argument("--help-extended", action="store_true", help="Show extended help (config schema, macros, examples) and exit.")

  # Structured config loading
  p.add_argument("--load", action="append", default=[], help="PATH_OR_GLOB of .json/.yaml/.yml. Deep-merge mapping docs into root context. Repeatable.")
  p.add_argument("--load-into", action="append", default=[], help="KEY=PATH_OR_GLOB of .json/.yaml/.yml. Assign parsed doc(s) to KEY. Repeatable.")

  # Scalars / JSON
  p.add_argument("--set", action="append", default=[], help="KEY=VALUE (nest with A.B=value). '@path' loads file text. Repeatable.")
  p.add_argument("--set-json", action="append", default=[], help="KEY=<json>. Repeatable.")
  p.add_argument("--set-json-file", action="append", default=[], help="KEY=/path/to/file.json (reads and parses JSON). Repeatable.")

  # Files (scalar or list via glob)
  p.add_argument("--set-file", action="append", default=[], help="KEY=/path/or/glob. 1 match -> scalar; many -> list. Repeatable.")

  # zsh-friendly array ops
  p.add_argument("--add", action="append", default=[], help="KEY=VALUE. Append VALUE (or '@file') to list KEY. Repeatable.")
  p.add_argument("--add-file", action="append", default=[], help="KEY=/path/or/glob. Append contents of matches to list KEY. Repeatable.")
  p.add_argument("--set-index", action="append", default=[], help="KEY:INDEX=VALUE. Set list element at INDEX. VALUE may be '@file'. Repeatable.")
  p.add_argument("--set-file-index", action="append", default=[], help="KEY:INDEX=/path. Set list element from file (exactly one match). Repeatable.")

  # Output / debug
  p.add_argument("--out", help="Write the rendered output to this file (otherwise print to stdout).")
  p.add_argument("--print-context", action="store_true", help="Print the merged context (JSON) to stderr for debugging.")
  return p


def _apply_load(ctx: Dict[str, Any], patterns):
  from .utils import deep_merge
  for pat in patterns or []:
    # Accept accidental "index=path" pairs (e.g., "0=/path/file.yaml")
    if isinstance(pat, str) and "=" in pat:
      k, v = pat.split("=", 1)
      if k.isdigit():
        pat = v
    docs = load_structured_glob(pat)
    for d in docs:
      if isinstance(d, dict):
        deep_merge(ctx, d)
      else:
        die(f"--load expects mapping documents; got {type(d).__name__} in {pat}")


def _apply_load_into(ctx: Dict[str, Any], pairs):
  from .context_ops import _set_nested
  for pair in pairs or []:
    # Accept dict-style entries coming directly from YAML (e.g. {"DATA": "./file.json"})
    if isinstance(pair, dict):
      for key, pat in pair.items():
        docs = load_structured_glob(pat)
        value = docs[0] if len(docs) == 1 else docs
        _set_nested(ctx, key, value)
      continue
    # Accept "KEY=PATH" strings (and ignore accidental "index=PATH")
    if isinstance(pair, str):
      if "=" in pair:
        key, pat = pair.split("=", 1)
        if key.isdigit():  # normalize "0=/path" -> treat as path-only (cannot assign without a key)
          # No valid key; we cannot assign into the context. Fall through to error.
          pass
        else:
          docs = load_structured_glob(pat)
          value = docs[0] if len(docs) == 1 else docs
          _set_nested(ctx, key, value)
          continue
    die(f"--load-into expects KEY=PATH_OR_GLOB, got: {pair}")


def main() -> None:
  p = build_argparser()
  args = p.parse_args()

  if args.help_extended:
    print(EXTENDED_HELP.strip()); return

  # Load config file (if any), then merge defaults into args
  cfg_path = find_config_path(args.config)
  if cfg_path:
    cfg = load_config(cfg_path)
    merge_config_into_args(args, cfg, base_dir=cfg_path.parent)

  # Build context
  ctx: Dict[str, Any] = {}
  # 1) structured config
  _apply_load(ctx, args.load)
  _apply_load_into(ctx, args.load_into)
  # 2) scalars/files/json
  apply_set_pairs(ctx, args.set)
  apply_set_file(ctx, args.set_file)
  apply_set_json(ctx, args.set_json)
  apply_set_json_file(ctx, args.set_json_file)
  # 3) zsh-friendly array ops
  apply_add(ctx, args.add)
  apply_add_file(ctx, args.add_file)
  apply_set_index(ctx, args.set_index)
  apply_set_file_index(ctx, args.set_file_index)

  if args.print_context:
    import sys
    sys.stderr.write(json.dumps(ctx, indent=2, ensure_ascii=False) + "\n")

  tpl_path = Path(args.template_name)
  if not tpl_path.exists():
    die(f"Template not found: {tpl_path}")

  rendered = render_template(tpl_path, ctx, args.template_search)

  if args.out:
    Path(args.out).write_text(rendered, encoding="utf-8")
  else:
    print(rendered, end="")
