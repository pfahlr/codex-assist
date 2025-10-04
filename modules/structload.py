from __future__ import annotations
import json, glob
from pathlib import Path
from typing import Any, List, Dict
from .utils import die, expand_path, read_text_file, load_pattern_contents
import os

_JSON_EXTS = {".json"}
_YAML_EXTS = {".yaml", ".yml"}

def _parse_json(text: str) -> Any:
  return json.loads(text)

def _parse_yaml_multi(text: str) -> List[Any]:
  try:
    import yaml  # type: ignore
  except Exception:
    die("YAML support requires PyYAML. Install with: pip install PyYAML")
  docs = [d for d in yaml.safe_load_all(text) if d is not None]
  return docs or [None]

def _abspath(base_dir: Path, p: str) -> str:
  p = expand_path(p)
  return p if os.path.isabs(p) else str((base_dir / p).resolve())

def _resolve_file_macros(node: Any, base_dir: Path) -> Any:
  """Recursively replace {$file/$files/$glob/$glob_one[,$join]} macros with file text(s),
  resolving relative paths against base_dir (the directory of the structured file)."""
  if isinstance(node, dict):
    if "$file" in node:
      return read_text_file(_abspath(base_dir, node["$file"]))
    if "$files" in node:
      paths = node["$files"]
      if not isinstance(paths, list):
        die("$files must be a list of paths")
      return [read_text_file(_abspath(base_dir, p)) for p in paths]
    if "$glob_one" in node:
      pattern = _abspath(base_dir, node["$glob_one"])
      texts = load_pattern_contents(pattern)
      if len(texts) != 1:
        die(f"$glob_one matched {len(texts)} files; expected exactly 1.")
      return texts[0]
    if "$glob" in node:
      pattern = _abspath(base_dir, node["$glob"])
      texts = load_pattern_contents(pattern)
      if "$join" in node:
        return str(node["$join"]).join(texts)
      return texts
    return {k: _resolve_file_macros(v, base_dir) for k, v in node.items()}
  if isinstance(node, list):
    return [_resolve_file_macros(v, base_dir) for v in node]
  return node

def load_structured_file(path: str) -> List[Any]:
  p = Path(expand_path(path))
  if not p.exists():
    die(f"Structured file not found: {p}")
  text, ext = p.read_text(encoding="utf-8"), p.suffix.lower()
  if ext in _JSON_EXTS:
    docs = [_parse_json(text)]
  elif ext in _YAML_EXTS:
    docs = _parse_yaml_multi(text)
  else:
    die(f"Unsupported structured file type for {p} (expected .json/.yaml/.yml)")
    return []
  return [_resolve_file_macros(d, p.parent) for d in docs]

def load_structured_glob(pattern: str) -> List[Any]:
  pat = expand_path(pattern)
  matches = sorted(glob.glob(pat, recursive=True))
  if not matches:
    return load_structured_file(pat)
  out: List[Any] = []
  for m in matches:
    out.extend(load_structured_file(m))
  return out
