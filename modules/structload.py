from __future__ import annotations
import json, glob
from pathlib import Path
from typing import Any, List, Dict
from .utils import die, expand_path, read_text_file, load_pattern_contents

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

def _resolve_file_macros(node: Any) -> Any:
  if isinstance(node, dict):
    if "$file" in node:
      return read_text_file(node["$file"])
    if "$files" in node:
      paths = node["$files"]
      if not isinstance(paths, list):
        die("$files must be a list of paths")
      return [read_text_file(p) for p in paths]
    if "$glob_one" in node:
      texts = load_pattern_contents(node["$glob_one"])
      if len(texts) != 1:
        die(f"$glob_one matched {len(texts)} files; expected exactly 1.")
      return texts[0]
    if "$glob" in node:
      texts = load_pattern_contents(node["$glob"])
      if "$join" in node:
        return str(node["$join"]).join(texts)
      return texts
    return {k: _resolve_file_macros(v) for k, v in node.items()}
  if isinstance(node, list):
    return [_resolve_file_macros(v) for v in node]
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
  return [_resolve_file_macros(d) for d in docs]

def load_structured_glob(pattern: str) -> List[Any]:
  pat = expand_path(pattern)
  matches = sorted(glob.glob(pat, recursive=True))
  if not matches:
    return load_structured_file(pat)
  out: List[Any] = []
  for m in matches:
    out.extend(load_structured_file(m))
  return out
