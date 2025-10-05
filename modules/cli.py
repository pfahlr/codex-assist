from __future__ import annotations
import argparse, json
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

with open('./docs/codex_prompt_builder.cli.help.md', 'r') as f:
  extended_help_text = f.read()

EXTENDED_HELP = extended_help_text

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
    if "=" not in pair:
      die(f"--load-into expects KEY=PATH_OR_GLOB, got: {pair}")
    key, pat = pair.split("=", 1)
    docs = load_structured_glob(pat)
    value = docs[0] if len(docs) == 1 else docs
    _set_nested(ctx, key, value)

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
