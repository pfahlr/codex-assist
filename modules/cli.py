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

with open('./docs/codex_prompt_builder.cli.help.md') as f:
  helptext = f.read()

EXTENDED_HELP = helptext

def build_argparser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(
    description="Render a Jinja2 template with values from CLI flags (modular Codex Assistant).",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=EXTENDED_HELP
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


def _strip_index_prefix(s: str) -> str:
  """Strip a leading '<digits>=' prefix if present, even for strings like '0=KEY=PATH'."""
  if "=" not in s:
    return s
  parts = s.split("=")
  if parts and parts[0].isdigit():
    return "=".join(parts[1:])
  return s


def _apply_load(ctx: Dict[str, Any], patterns, *, optional: bool):
  from .utils import deep_merge
  for pat in patterns or []:
    if isinstance(pat, str):
      pat = _strip_index_prefix(pat)
    docs = load_structured_glob(pat, optional=optional)
    for d in docs:
      if isinstance(d, dict):
        deep_merge(ctx, d)
      else:
        die(f"--load expects mapping documents; got {type(d).__name__} in {pat}")


def _apply_load_into(ctx: Dict[str, Any], pairs, *, optional: bool):
  from .context_ops import _set_nested
  for pair in pairs or []:
    # Dict-style entries coming directly from YAML (e.g. {"DATA": "./file.json"})
    if isinstance(pair, dict):
      for key, pat in pair.items():
        docs = load_structured_glob(pat, optional=optional)
        if not docs:
          continue  # optional and missing -> skip
        value = docs[0] if len(docs) == 1 else docs
        _set_nested(ctx, key, value)
      continue

    # String entries: support accidental index prefix AND KEY=PATH
    if isinstance(pair, str):
      s = _strip_index_prefix(pair)
      if "=" in s:
        key, pat = s.split("=", 1)
        if key:
          docs = load_structured_glob(pat, optional=optional)
          if not docs:
            continue  # optional and missing -> skip
          value = docs[0] if len(docs) == 1 else docs
          _set_nested(ctx, key, value)
          continue

    die(f"--load-into expects KEY=PATH_OR_GLOB, got: {pair}")


def main() -> None:
  p = build_argparser()
  args = p.parse_args()

  print(EXTENDED_HELP)
  print(args)

  if args.help_extended:
    print(EXTENDED_HELP.strip()); return

  # Load config file (if any), then merge defaults into args
  cfg_path = find_config_path(args.config)
  if cfg_path:
    cfg = load_config(cfg_path)
    merge_config_into_args(args, cfg, base_dir=cfg_path.parent)

  # Determine optionality:
  # If args.load/args.load_into came from config (not CLI), merge_config_into_args
  # will have set these flags to True. Otherwise they default to False.
  load_optional = getattr(args, "_load_optional", False)
  load_into_optional = getattr(args, "_load_into_optional", False)

  # Build context
  ctx: Dict[str, Any] = {}
  # 1) structured config
  _apply_load(ctx, args.load, optional=load_optional)
  _apply_load_into(ctx, args.load_into, optional=load_into_optional)
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
