from __future__ import annotations
from typing import Any, Dict, List
from .utils import (
  die, maybe_file_value, load_pattern_contents,
  _ARRAY_KEY_RE, _COLON_INDEX_RE
)

def _ensure_path_dict(ctx: Dict[str, Any], parts: List[str]) -> Dict[str, Any]:
  cur: Dict[str, Any] = ctx
  for p in parts:
    if p not in cur or not isinstance(cur[p], dict):
      cur[p] = {}
    cur = cur[p]  # type: ignore[assignment]
  return cur

def _set_nested(ctx: Dict[str, Any], dotted_key: str, value: Any) -> None:
  parts = dotted_key.split(".")
  parent = _ensure_path_dict(ctx, parts[:-1])
  parent[parts[-1]] = value

def _ensure_list_at(ctx: Dict[str, Any], dotted: str) -> List[Any]:
  parts = dotted.split(".")
  parent = _ensure_path_dict(ctx, parts[:-1])
  key = parts[-1]
  if key not in parent:
    parent[key] = []
  if not isinstance(parent[key], list):
    die(f"Cannot assign list semantics to non-list key '{dotted}'")
  return parent[key]  # type: ignore[return-value]

def apply_set_pairs(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set expects KEY=VALUE, got: {pair}")
    key, raw_value = pair.split("=", 1)
    value = maybe_file_value(raw_value)
    parts, last = key.split("."), key.split(".")[-1]
    m = _ARRAY_KEY_RE.match(last)
    if not m:
      _set_nested(ctx, key, value); continue
    arr_name, idx = m.group("name"), m.group("index")
    if idx is None:
      _set_nested(ctx, key, value); continue
    arr_path = ".".join(parts[:-1] + [arr_name])
    lst = _ensure_list_at(ctx, arr_path)
    if idx == "":
      lst.append(value)
    else:
      i = int(idx)
      if len(lst) <= i: lst.extend([None] * (i + 1 - len(lst)))
      lst[i] = value

def apply_set_json(ctx: Dict[str, Any], pairs: List[str]) -> None:
  import json
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
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-file expects KEY=/path, got: {pair}")
    key, pattern = pair.split("=", 1)
    contents = load_pattern_contents(pattern)
    parts, last = key.split("."), key.split(".")[-1]
    m = _ARRAY_KEY_RE.match(last)
    if not m:
      _set_nested(ctx, key, contents[0] if len(contents) == 1 else contents); continue
    arr_name, idx = m.group("name"), m.group("index")
    if idx is None:
      _set_nested(ctx, key, contents[0] if len(contents) == 1 else contents); continue
    arr_path = ".".join(parts[:-1] + [arr_name])
    lst = _ensure_list_at(ctx, arr_path)
    if idx == "":
      lst.extend(contents)
    else:
      if len(contents) != 1:
        die(f"--set-file {key}=<glob> matched {len(contents)} files; expected exactly 1.")
      i = int(idx)
      if len(lst) <= i: lst.extend([None] * (i + 1 - len(lst)))
      lst[i] = contents[0]

def apply_set_json_file(ctx: Dict[str, Any], pairs: List[str]) -> None:
  from .utils import read_text_file, expand_path
  import json
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

def apply_add(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--add expects KEY=VALUE, got: {pair}")
    key, raw_value = pair.split("=", 1)
    value = maybe_file_value(raw_value)
    _ensure_list_at(ctx, key).append(value)

def apply_add_file(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--add-file expects KEY=/path, got: {pair}")
    key, pattern = pair.split("=", 1)
    _ensure_list_at(ctx, key).extend(load_pattern_contents(pattern))

def apply_set_index(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-index expects KEY:INDEX=VALUE, got: {pair}")
    key_part, raw_value = pair.split("=", 1)
    m = _COLON_INDEX_RE.match(key_part)
    if not m: die(f"--set-index requires KEY:INDEX form, got: {key_part}")
    base_key, index = m.group("name"), int(m.group("index"))
    value = maybe_file_value(raw_value)
    lst = _ensure_list_at(ctx, base_key)
    if len(lst) <= index: lst.extend([None] * (index + 1 - len(lst)))
    lst[index] = value

def apply_set_file_index(ctx: Dict[str, Any], pairs: List[str]) -> None:
  for pair in pairs or []:
    if "=" not in pair:
      die(f"--set-file-index expects KEY:INDEX=/path, got: {pair}")
    key_part, pattern = pair.split("=", 1)
    m = _COLON_INDEX_RE.match(key_part)
    if not m: die(f"--set-file-index requires KEY:INDEX form, got: {key_part}")
    base_key, index = m.group("name"), int(m.group("index"))
    contents = load_pattern_contents(pattern)
    if len(contents) != 1:
      die(f"--set-file-index {key_part}=<glob> matched {len(contents)} files; expected exactly 1.")
    lst = _ensure_list_at(ctx, base_key)
    if len(lst) <= index: lst.extend([None] * (index + 1 - len(lst)))
    lst[index] = contents[0]

