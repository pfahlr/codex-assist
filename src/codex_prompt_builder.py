#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2-space indentation style throughout.

"""
codex_template_builder.py
-------------------------
Render text files from Jinja2 templates using simple CLI parameters.

Why this exists
===============
You often need to generate repeatable prompts/comments/scripts where most
content is boilerplate and only a few variables change. This script lets you
keep the boilerplate in a template and set values at render time.

Features
========
- Use --template-name to point to any Jinja2 template file.
- Fill in scalar values with repeated:       --set KEY=VALUE
- Build arrays with append:                  --set LIST[]=item
- Or set by index:                           --set LIST[2]=item
- Create nested objects via dot notation:    --set PARENT.CHILD=value
- Inject raw JSON into the context:          --set-json KEY='["a","b"]'
- Merge multiple --set / --set-json flags.
- Optional: print the merged context for debugging.
- Adds a 'zip' filter so you can iterate two arrays in parallel.
  Example in your template:
    {% for a, b in A|zip(B) %} ... {% endfor %}

Requirements
============
  pip install Jinja2

Examples
========
1) Scalars + arrays built from CLI:
   python codex_template_builder.py \\
     --template-name templates/codex_consolidate.tpl \\
     --set OWNER=pfahlr --set REPO=ragx \\
     --set TOKEN_ENVVAR=CODEX_READ_ALL_REPOSITORIES_TOKEN \\
     --set BRANCHES[]=codex/fix-a --set BRANCHES[]=codex/fix-b \\
     --set BUG_IDS[]=B1 --set BUG_TEXTS[]='First bug' \\
     --set BUG_IDS[]=B2 --set BUG_TEXTS[]='Second bug' \\
     --out prompt.txt

2) JSON-friendly (clearer for complex data):
   python codex_template_builder.py \\
     --template-name templates/codex_consolidate.tpl \\
     --set OWNER=pfahlr --set REPO=ragx \\
     --set TOKEN_ENVVAR=CODEX_READ_ALL_REPOSITORIES_TOKEN \\
     --set-json BRANCHES='["codex/fix-a","codex/fix-b"]' \\
     --set-json BUGS='[{"id":"B1","text":"Bug one"},{"id":"B2","text":"Bug two"}]' \\
     --out prompt.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


# -----------------------------
# Utilities
# -----------------------------

def die(msg: str, exit_code: int = 2) -> None:
  """Print an error to stderr and exit."""
  sys.stderr.write(f"ERROR: {msg}\n")
  raise SystemExit(exit_code)


def ensure_jinja2() -> None:
  """Ensure Jinja2 is importable; explain how to install otherwise."""
  try:
    import jinja2  # type: ignore
  except Exception:
    die("Jinja2 is required. Install with: pip install Jinja2")


def deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
  """Recursively merge src into dst; returns dst for chaining."""
  for k, v in src.items():
    if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
      deep_merge(dst[k], v)
    else:
      dst[k] = v
  return dst


# -----------------------------
# Parsing CLI key-value inputs
# -----------------------------

_ARRAY_KEY_RE = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:\[(?P<index>\d*)\])?$")


def _set_nested(ctx: Dict[str, Any], dotted_key: str, value: Any) -> None:
  """Set a value into a nested dict using dot notation in the key."""
  parts = dotted_key.split(".")
  cur: Dict[str, Any] = ctx
  for p in parts[:-1]:
    if p not in cur or not isinstance(cur[p], dict):
      cur[p] = {}
    cur = cur[p]  # type: ignore[assignment]
  cur[parts[-1]] = value


def parse_set_pairs(pairs: List[str]) -> Dict[str, Any]:
  """Parse repeated --set KEY=VALUE parameters into a nested context dict.

  Supports:
    VAR=value                   -> ctx["VAR"] = "value"
    LIST[]=item                 -> ctx["LIST"] = ["item", ...] (append)
    LIST[2]=item                -> ctx["LIST"][2] = "item"  (auto-grows list)
    NESTED.PATH=value           -> ctx["NESTED"]["PATH"] = "value"
  """
  ctx: Dict[str, Any] = {}

  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set expects KEY=VALUE, got: {pair}")
    key, value = pair.split("=", 1)

    # Support nesting via dots on the full key, but bracket array syntax only on the last segment
    parts = key.split(".")
    last = parts[-1]

    m = _ARRAY_KEY_RE.match(last)
    if not m:
      _set_nested(ctx, key, value)
      continue

    arr_name = m.group("name")
    idx = m.group("index")  # None, "" (append), or digits

    if idx is None:
      # Plain scalar for this last segment
      _set_nested(ctx, key, value)
      continue

    # We have bracket syntax; arrays live at the final segment without the brackets
    arr_path = parts[:-1] + [arr_name]

    # Navigate/create the dict path up to the list
    cur: Dict[str, Any] = ctx
    for p in arr_path[:-1]:
      if p not in cur or not isinstance(cur[p], dict):
        cur[p] = {}
      cur = cur[p]  # type: ignore[assignment]

    # Ensure the list exists
    arr_key = arr_path[-1]
    if arr_key not in cur:
      cur[arr_key] = []
    if not isinstance(cur[arr_key], list):
      die(f"Cannot assign list semantics to non-list key '{arr_key}'")
    lst: List[Any] = cur[arr_key]  # type: ignore[assignment]

    if idx == "":
      # Append: LIST[]=value
      lst.append(value)
    else:
      # Explicit index: LIST[2]=value
      i = int(idx)
      if len(lst) <= i:
        lst.extend([None] * (i + 1 - len(lst)))
      lst[i] = value

  return ctx


def parse_set_json(pairs: List[str]) -> Dict[str, Any]:
  """Parse repeated --set-json KEY=<json> parameters."""
  ctx: Dict[str, Any] = {}
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-json expects KEY=<json>, got: {pair}")
    key, raw = pair.split("=", 1)
    try:
      value = json.loads(raw)
    except Exception as e:
      die(f"Invalid JSON for key '{key}': {e}")
    _set_nested(ctx, key, value)
  return ctx


# -----------------------------
# Rendering
# -----------------------------

def render_template(template_path: Path, context: Dict[str, Any]) -> str:
  """Render a Jinja2 template with the provided context."""
  ensure_jinja2()
  import jinja2  # imported late so help text prints fast without Jinja2 installed

  env = jinja2.Environment(
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
  )
  # Helpful filter: zip two lists together for parallel iteration
  env.filters['zip'] = lambda a, b: list(zip(a or [], b or []))

  source = template_path.read_text(encoding="utf-8")
  template = env.from_string(source)
  return template.render(**context)


# -----------------------------
# CLI
# -----------------------------

def build_argparser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(
    description="Render a Jinja2 template with values from --set / --set-json.",
    formatter_class=argparse.RawTextHelpFormatter,
  )
  p.add_argument("--template-name", required=True, help="Path to the Jinja2 template file.")
  p.add_argument("--set", action="append", default=[], help="KEY=VALUE (arrays: LIST[]=v, LIST[2]=v; nesting: A.B=v). Repeatable.")
  p.add_argument("--set-json", action="append", default=[], help="KEY=<json>. Repeatable.")
  p.add_argument("--out", help="Write the rendered output to this file (otherwise print to stdout)." )
  p.add_argument("--print-context", action="store_true", help="Print the merged context (JSON) to stderr for debugging.")
  return p


def main() -> None:
  args = build_argparser().parse_args()

  # Build context from sets
  ctx: Dict[str, Any] = {}
  deep_merge(ctx, parse_set_pairs(args.set))
  deep_merge(ctx, parse_set_json(args.set_json))

  if args.print_context:
    sys.stderr.write(json.dumps(ctx, indent=2, ensure_ascii=False) + "\n")

  tpl_path = Path(args.template_name)
  if not tpl_path.exists():
    die(f"Template not found: {tpl_path}")

  rendered = render_template(tpl_path, ctx)

  if args.out:
    Path(args.out).write_text(rendered, encoding="utf-8")
  else:
    sys.stdout.write(rendered)


if __name__ == "__main__":
  main()
