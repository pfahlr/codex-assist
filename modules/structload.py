from __future__ import annotations

import glob
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from .utils import die, expand_path, read_text_file


def _parse_json(text: str) -> Any:
  try:
    return json.loads(text)
  except Exception as e:
    die(f"Invalid JSON: {e}")
  return None  # unreachable


def _parse_yaml(text: str) -> List[Any]:
  try:
    import yaml  # type: ignore
  except Exception:
    die("YAML support requires PyYAML. Install with: pip install PyYAML")
  try:
    docs = list(yaml.safe_load_all(text))  # type: ignore[attr-defined]
  except Exception as e:
    die(f"Invalid YAML: {e}")
  return docs


def _read_file_text_resolve(base_dir: Path, path_str: str) -> str:
  """Read UTF-8 text from a path that may be relative to base_dir."""
  p = Path(expand_path(path_str))
  if not p.is_absolute():
    p = (base_dir / p).resolve()
  return read_text_file(str(p))


def _glob_matches_resolve(base_dir: Path, pattern: str) -> List[Path]:
  """Glob with lexicographic sort; resolve relative to base_dir."""
  pat = expand_path(pattern)
  if not os.path.isabs(pat):
    pat = str((base_dir / pat).resolve())
  # glob returns plain strings; normalize to Path and sort
  matches = sorted(glob.glob(pat, recursive=True))
  return [Path(m) for m in matches]


def _apply_macros(node: Any, base_dir: Path) -> Any:
  """Recursively apply $file/$files/$glob/$glob_one (and optional $join)."""
  if isinstance(node, dict):
    # Macro object?
    keys = set(node.keys())
    # $file
    if "$file" in keys:
      path = node["$file"]
      if not isinstance(path, str):
        die("$file expects a string path")
      return _read_file_text_resolve(base_dir, path)

    # $files
    if "$files" in keys:
      arr = node["$files"]
      if not isinstance(arr, list):
        die("$files expects a list of paths")
      return [_read_file_text_resolve(base_dir, p) for p in arr]

    # $glob / $glob_one (with optional $join)
    if "$glob_one" in keys:
      pattern = node["$glob_one"]
      if not isinstance(pattern, str):
        die("$glob_one expects a string pattern")
      matches = _glob_matches_resolve(base_dir, pattern)
      if len(matches) == 0:
        die(f"$glob_one found no matches for: {pattern}")
      if len(matches) > 1:
        die(f"$glob_one expected exactly 1 match, found {len(matches)} for: {pattern}")
      return matches[0].read_text(encoding="utf-8")

    if "$glob" in keys:
      pattern = node["$glob"]
      if not isinstance(pattern, str):
        die("$glob expects a string pattern")
      matches = _glob_matches_resolve(base_dir, pattern)
      texts = [m.read_text(encoding="utf-8") for m in matches]
      if "$join" in keys:
        sep = node["$join"]
        if not isinstance(sep, str):
          die("$join expects a string separator")
        return sep.join(texts)
      return texts

    # Not a macro object: recurse into mapping values
    return {k: _apply_macros(v, base_dir) for k, v in node.items()}

  if isinstance(node, list):
    return [_apply_macros(v, base_dir) for v in node]

  return node


def load_structured_file(path_str: str) -> List[Any]:
  """Load a .json/.yaml/.yml file and return a list of documents (1 for JSON)."""
  p = Path(expand_path(path_str))
  if not p.exists():
    die(f"Structured file not found: {p}")
  text = p.read_text(encoding="utf-8")
  suffix = p.suffix.lower()

  if suffix == ".json":
    docs = [_parse_json(text)]
  elif suffix in (".yaml", ".yml"):
    docs = _parse_yaml(text)
  else:
    # Fallback heuristic: try JSON then YAML
    try:
      docs = [_parse_json(text)]
    except SystemExit:
      # JSON failed with die -> try YAML
      docs = _parse_yaml(text)

  base_dir = p.parent
  return [_apply_macros(doc, base_dir) for doc in docs]


def load_structured_glob(pattern: str) -> List[Any]:
  """Load one or more structured files via glob pattern. If no glob match,
  treat input as a single file path.
  """
  pat = expand_path(pattern)
  matches = sorted(glob.glob(pat, recursive=True))
  out: List[Any] = []
  if matches:
    for m in matches:
      out.extend(load_structured_file(m))
    return out
  # No glob matches: treat as single file path and load (will die if missing)
  return load_structured_file(pat)
