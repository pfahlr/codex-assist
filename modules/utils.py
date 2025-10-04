from __future__ import annotations
import os, sys, glob, json, re
from pathlib import Path
from typing import Any, Dict, List

def die(msg: str, exit_code: int = 2) -> None:
  sys.stderr.write(f"ERROR: {msg}\n")
  raise SystemExit(exit_code)

def ensure_jinja2() -> None:
  try:
    import jinja2  # noqa: F401
  except Exception:
    die("Jinja2 is required. Install with: pip install Jinja2")

def expand_path(p: str) -> str:
  return os.path.expandvars(os.path.expanduser(p))

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
  pat = expand_path(pattern)
  matches = sorted(glob.glob(pat, recursive=True))
  if matches:
    return [read_text_file(m) for m in matches]
  return [read_text_file(pat)]

def maybe_file_value(raw_value: str) -> str:
  if raw_value.startswith("@@"):
    return raw_value[1:]
  if raw_value.startswith("@"):
    path = raw_value[1:]
    if not path:
      die("Empty path after '@' in value. Use @@ to escape a literal '@'.")
    return read_text_file(expand_path(path))
  return raw_value

def deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
  for k, v in src.items():
    if isinstance(v, dict) and isinstance(dst.get(k), dict):
      deep_merge(dst[k], v)  # type: ignore[index]
    else:
      dst[k] = v
  return dst

_ARRAY_KEY_RE = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:\[(?P<index>\d*)\])?$")
_COLON_INDEX_RE = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_.]*):(?P<index>\d+)$")
