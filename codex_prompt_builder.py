#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2-space indentation style throughout.

"""
codex_template_builder.py
-------------------------
Render text files from Jinja2 templates using simple CLI parameters.

Array-safe, zsh-friendly additions:
- --add KEY=VALUE                    # append VALUE to list KEY (VALUE may be '@file')
- --add-file KEY=/path/glob*.txt     # append contents of each match to list KEY
- --set-index KEY:2=VALUE            # set KEY[2] to VALUE (VALUE may be '@file')
- --set-file-index KEY:2=/path.txt   # set KEY[2] from a single file

Existing (kept for compatibility):
- --set KEY=VALUE                    # scalars; also supports '@file' shorthand
- --set-file KEY=/path/or/glob       # 1 match -> scalar; many -> list
- --set-json KEY=<json>
- --set-json-file KEY=/path.json

Includes & template helpers:
- Native Jinja includes: {% include "partials/foo.tpl" %}
- Raw file helpers in templates:
    {{ include_text("docs/intro.md") }}
    {{ read_file("snippets/step.txt") }}                 # alias of include_text
    {{ include_text_glob("notes/*.md", sep="\n\n") }}
    {% for p in glob_paths("snips/*.md") %}{{ include_text(p) }}{% endfor %}
    {{ read_json("data/spec.json").title }}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import glob
from pathlib import Path
from typing import Any, Dict, List, Sequence

# -----------------------------
# Utilities
# -----------------------------

def die(msg: str, exit_code: int = 2) -> None:
  sys.stderr.write(f"ERROR: {msg}\n")
  raise SystemExit(exit_code)

def ensure_jinja2() -> None:
  try:
    import jinja2  # type: ignore
  except Exception:
    die("Jinja2 is required. Install with: pip install Jinja2")

def expand_path(pattern: str) -> str:
  return os.path.expandvars(os.path.expanduser(pattern))

def read_text_file(path_str: str) -> str:
  p = Path(expand_path(path_str))
  if not p.exists():
    die(f"File not found: {p}")
  try:
    return p.read_text(encoding="utf-8")
  except Exception as e:
    die(f"Failed to read text file '{p}': {e}")
  return ""  # unreachable

def load_pattern_contents(pattern: str) -> List[str]:
  pattern = expand_path(pattern)
  matches = sorted(glob.glob(pattern, recursive=True))
  if matches:
    return [read_text_file(m) for m in matches]
  # Treat as single file path when glob finds nothing
  return [read_text_file(pattern)]

def maybe_file_value(raw_value: str) -> str:
  # '@@foo' -> '@foo' (escape)
  if raw_value.startswith("@@"):
    return raw_value[1:]
  # '@path' -> load text
  if raw_value.startswith("@"):
    path = raw_value[1:]
    if not path:
      die("Empty path after '@' in value. Use @@ to escape a literal '@'.")
    return read_text_file(expand_path(path))
  return raw_value

# -----------------------------
# Nested/array helpers
# -----------------------------

_ARRAY_KEY_RE = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:\[(?P<index>\d*)\])?$")
_COLON_INDEX_RE = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_.]*):(?P<index>\d+)$")

def _ensure_path_dict(ctx: Dict[str, Any], path_parts: List[str]) -> Dict[str, Any]:
  cur: Dict[str, Any] = ctx
  for p in path_parts:
    if p not in cur or not isinstance(cur[p], dict):
      cur[p] = {}
    cur = cur[p]  # type: ignore[assignment]
  return cur

def _set_nested(ctx: Dict[str, Any], dotted_key: str, value: Any) -> None:
  parts = dotted_key.split(".")
  parent = _ensure_path_dict(ctx, parts[:-1])
  parent[parts[-1]] = value

def _ensure_list_at(ctx: Dict[str, Any], dotted_key_wo_brackets: str) -> List[Any]:
  parts = dotted_key_wo_brackets.split(".")
  parent = _ensure_path_dict(ctx, parts[:-1])
  key = parts[-1]
  if key not in parent:
    parent[key] = []
  if not isinstance(parent[key], list):
    die(f"Cannot assign list semantics to non-list key '{dotted_key_wo_brackets}'")
  return parent[key]  # type: ignore[return-value]

# -----------------------------
# Apply functions (mutate ctx)
# -----------------------------

def apply_set_pairs(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --set KEY=VALUE (supports KEY=@file, old KEY[]/KEY[2] forms)
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set expects KEY=VALUE, got: {pair}")
    key, raw_value = pair.split("=", 1)
    value = maybe_file_value(raw_value)

    parts = key.split(".")
    last = parts[-1]
    m = _ARRAY_KEY_RE.match(last)
    if not m:
      _set_nested(ctx, key, value)
      continue

    arr_name = m.group("name")
    idx = m.group("index")  # None, "" (append), or digits
    if idx is None:
      _set_nested(ctx, key, value)
      continue

    arr_path = ".".join(parts[:-1] + [arr_name])
    lst = _ensure_list_at(ctx, arr_path)
    if idx == "":
      lst.append(value)
    else:
      i = int(idx)
      if len(lst) <= i:
        lst.extend([None] * (i + 1 - len(lst)))
      lst[i] = value

def apply_set_json(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-json expects KEY=<json>, got: {pair}")
    key, raw = pair.split("=", 1)
    try:
      value = json.loads(raw)
    except Exception as e:
      die(f"Invalid JSON for key '{key}': {e}")
    _set_nested(ctx, key, value)

def apply_set_file(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --set-file KEY=PATH_OR_GLOB
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-file expects KEY=/path, got: {pair}")
    key, pattern = pair.split("=", 1)
    contents = load_pattern_contents(pattern)

    parts = key.split(".")
    last = parts[-1]
    m = _ARRAY_KEY_RE.match(last)
    if not m:
      # No array syntax. If multiple files matched, set list; else scalar.
      _set_nested(ctx, key, contents[0] if len(contents) == 1 else contents)
      continue

    arr_name = m.group("name")
    idx = m.group("index")  # None, "" (append), or digits
    if idx is None:
      _set_nested(ctx, key, contents[0] if len(contents) == 1 else contents)
      continue

    arr_path = ".".join(parts[:-1] + [arr_name])
    lst = _ensure_list_at(ctx, arr_path)
    if idx == "":
      lst.extend(contents)
    else:
      if len(contents) != 1:
        die(f"--set-file {key}=<glob> matched {len(contents)} files; expected exactly 1 for explicit index.")
      i = int(idx)
      if len(lst) <= i:
        lst.extend([None] * (i + 1 - len(lst)))
      lst[i] = contents[0]

def apply_set_json_file(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-json-file expects KEY=/path/to/file.json, got: {pair}")
    key, path_str = pair.split("=", 1)
    raw = read_text_file(expand_path(path_str))
    try:
      value = json.loads(raw)
    except Exception as e:
      die(f"Invalid JSON in file for key '{key}': {e}")
    _set_nested(ctx, key, value)

# NEW: zsh-friendly array builders
def apply_add(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --add KEY=VALUE  (append VALUE to list KEY; VALUE may be '@file')
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--add expects KEY=VALUE, got: {pair}")
    key, raw_value = pair.split("=", 1)
    value = maybe_file_value(raw_value)
    lst = _ensure_list_at(ctx, key)
    lst.append(value)

def apply_add_file(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --add-file KEY=/path/glob   (append contents of each match to list KEY)
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--add-file expects KEY=/path, got: {pair}")
    key, pattern = pair.split("=", 1)
    contents = load_pattern_contents(pattern)
    lst = _ensure_list_at(ctx, key)
    lst.extend(contents)

def apply_set_index(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --set-index KEY:2=VALUE     (VALUE may be '@file')
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-index expects KEY:INDEX=VALUE, got: {pair}")
    key_part, raw_value = pair.split("=", 1)
    m = _COLON_INDEX_RE.match(key_part)
    if not m:
      die(f"--set-index requires KEY:INDEX form, got: {key_part}")
    base_key = m.group("name")    # may include dots for nesting
    index = int(m.group("index"))
    value = maybe_file_value(raw_value)
    lst = _ensure_list_at(ctx, base_key)
    if len(lst) <= index:
      lst.extend([None] * (index + 1 - len(lst)))
    lst[index] = value

def apply_set_file_index(ctx: Dict[str, Any], pairs: List[str]) -> None:
  # --set-file-index KEY:2=/path.txt  (exactly one file must match)
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-file-index expects KEY:INDEX=/path, got: {pair}")
    key_part, pattern = pair.split("=", 1)
    m = _COLON_INDEX_RE.match(key_part)
    if not m:
      die(f"--set-file-index requires KEY:INDEX form, got: {key_part}")
    base_key = m.group("name")
    index = int(m.group("index"))
    contents = load_pattern_contents(pattern)
    if len(contents) != 1:
      die(f"--set-file-index {key_part}=<glob> matched {len(contents)} files; expected exactly 1.")
    lst = _ensure_list_at(ctx, base_key)
    if len(lst) <= index:
      lst.extend([None] * (index + 1 - len(lst)))
    lst[index] = contents[0]

# -----------------------------
# Include helpers for templates
# -----------------------------

def _dedupe_keep_order(items: Sequence[str]) -> List[str]:
  seen = set()
  out: List[str] = []
  for it in items:
    if it not in seen:
      seen.add(it)
      out.append(it)
  return out

def _resolve_path_for_include(base_dirs: List[str], path_str: str) -> Path:
  p = Path(expand_path(path_str))
  if p.is_absolute() and p.exists():
    return p
  if p.exists():
    return p
  for base in base_dirs:
    cand = Path(base) / path_str
    if cand.exists():
      return cand
  die(f"Include path not found: {path_str} (searched: {', '.join(base_dirs)})")
  return p  # unreachable

def _make_include_helpers(base_dirs: List[str]):
  def include_text(path: str) -> str:
    p = _resolve_path_for_include(base_dirs, path)
    return p.read_text(encoding="utf-8")

  def read_file(path: str) -> str:
    return include_text(path)

  def include_text_glob(pattern: str, sep: str = "\n") -> str:
    pat = expand_path(pattern)
    matches = sorted(glob.glob(pat, recursive=True))
    if not matches:
      for base in base_dirs:
        matches = sorted(glob.glob(str(Path(base) / pattern), recursive=True))
        if matches:
          break
    if not matches:
      die(f"include_text_glob found no matches for pattern: {pattern}")
    return sep.join(Path(m).read_text(encoding="utf-8") for m in matches)

  def glob_paths(pattern: str) -> List[str]:
    pat = expand_path(pattern)
    matches = sorted(glob.glob(pat, recursive=True))
    if not matches:
      all_matches: List[str] = []
      for base in base_dirs:
        all_matches.extend(glob.glob(str(Path(base) / pattern), recursive=True))
      matches = sorted(set(all_matches))
    return matches

  def read_json(path: str) -> Any:
    p = _resolve_path_for_include(base_dirs, path)
    try:
      return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
      die(f"Failed to parse JSON include '{path}': {e}")
    return None  # unreachable

  return include_text, read_file, include_text_glob, glob_paths, read_json

# -----------------------------
# Rendering (loader + helpers)
# -----------------------------

def render_template(template_path: Path, context: Dict[str, Any], extra_search: List[str]) -> str:
  ensure_jinja2()
  import jinja2  # type: ignore
  from jinja2 import FileSystemLoader, ChoiceLoader

  base_dir = str(template_path.parent.resolve())
  search_paths = _dedupe_keep_order([base_dir] + [str(Path(p).resolve()) for p in extra_search] + [os.getcwd()])

  loader = ChoiceLoader([FileSystemLoader(search_paths)])
  env = jinja2.Environment(
    loader=loader,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
  )
  env.filters['zip'] = lambda a, b: list(zip(a or [], b or []))

  include_text, read_file, include_text_glob, glob_paths, read_json = _make_include_helpers(search_paths)
  env.globals.update({
    'include_text': include_text,
    'read_file': read_file,
    'include_text_glob': include_text_glob,
    'glob_paths': glob_paths,
    'read_json': read_json,
  })

  template = env.get_template(template_path.name)
  return template.render(**context)

# -----------------------------
# CLI
# -----------------------------

def build_argparser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(
    description="Render a Jinja2 template with values from CLI flags (zsh-friendly array builders + includes).",
    formatter_class=argparse.RawTextHelpFormatter,
  )
  p.add_argument("--template-name", required=True, help="Path to the Jinja2 template file.")
  p.add_argument("--template-search", action="append", default=[], help="Additional template/include search paths. Repeatable.")
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

def main() -> None:
  args = build_argparser().parse_args()

  ctx: Dict[str, Any] = {}
  # Order matters: later flags can override earlier ones if they set scalars,
  # while appends always extend lists.
  apply_set_pairs(ctx, args.set)
  apply_set_file(ctx, args.set_file)
  apply_set_json(ctx, args.set_json)
  apply_set_json_file(ctx, args.set_json_file)
  # zsh-friendly array builders
  apply_add(ctx, args.add)
  apply_add_file(ctx, args.add_file)
  apply_set_index(ctx, args.set_index)
  apply_set_file_index(ctx, args.set_file_index)

  if args.print_context:
    sys.stderr.write(json.dumps(ctx, indent=2, ensure_ascii=False) + "\n")

  tpl_path = Path(args.template_name)
  if not tpl_path.exists():
    die(f"Template not found: {tpl_path}")

  rendered = render_template(tpl_path, ctx, args.template_search)

  if args.out:
    Path(args.out).write_text(rendered, encoding="utf-8")
  else:
    sys.stdout.write(rendered)

if __name__ == "__main__":
  main()
