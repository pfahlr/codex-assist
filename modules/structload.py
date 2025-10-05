from __future__ import annotations

import glob
import json
import os
from pathlib import Path
from typing import Any, List

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
  p = Path(expand_path(path_str))
  if not p.is_absolute():
    p = (base_dir / p).resolve()
  return read_text_file(str(p))


def _glob_matches_resolve(base_dir: Path, pattern: str) -> List[Path]:
  pat = expand_path(pattern)
  if not os.path.isabs(pat):
    pat = str((base_dir / pat).resolve())
  matches = sorted(glob.glob(pat, recursive=True))
  return [Path(m) for m in matches]


def _apply_macros(node: Any, base_dir: Path) -> Any:
  """Recursively apply $file/$files/$glob/$glob_one (and optional $join)."""
  if isinstance(node, dict):
    keys = set(node.keys())

    if "$file" in keys:
      path = node["$file"]
      if not isinstance(path, str):
        die("$file expects a string path")
      return _read_file_text_resolve(base_dir, path)

    if "$files" in keys:
      arr = node["$files"]
      if not isinstance(arr, list):
        die("$files expects a list of paths")
      return [_read_file_text_resolve(base_dir, p) for p in arr]

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
      docs = _parse_yaml(text)

  base_dir = p.parent
  return [_apply_macros(doc, base_dir) for doc in docs]


def load_structured_glob(pattern: str, *, optional: bool = False) -> List[Any]:
  """Load one or more structured files via glob pattern.

  Behavior:
    - If pattern has glob magic and matches files -> load all (sorted).
    - If pattern has glob magic but matches none:
        * optional=True  -> return []
        * optional=False -> error
    - If pattern is a single path:
        * exists -> load it
        * missing:
            optional=True  -> return []
            optional=False -> error
  """
  pat = expand_path(pattern)
  has_magic = glob.has_magic(pat)

  if has_magic:
    matches = sorted(glob.glob(pat, recursive=True))
    if not matches:
      if optional:
        return []
      die(f"Structured file not found: {pat}")
    out: List[Any] = []
    for m in matches:
      out.extend(load_structured_file(m))
    return out

  # Single file path
  p = Path(pat)
  if not p.exists():
    if optional:
      return []
    die(f"Structured file not found: {p}")
  return load_structured_file(pat)
