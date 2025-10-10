from __future__ import annotations
import os, glob, json
from pathlib import Path
from typing import Any, List, Sequence
from .utils import ensure_jinja2, expand_path, die
from .jinja_filters import register_filters

def _dedupe_keep_order(items: Sequence[str]) -> List[str]:
  seen, out = set(), []
  for it in items:
    if it not in seen:
      seen.add(it); out.append(it)
  return out

def _resolve_path_for_include(base_dirs: List[str], path_str: str) -> Path:
  p = Path(expand_path(path_str))
  if p.is_absolute() and p.exists(): return p
  if p.exists(): return p
  for base in base_dirs:
    cand = Path(base) / path_str
    if cand.exists(): return cand
  die(f"Include path not found: {path_str} (searched: {', '.join(base_dirs)})")
  return p

def _make_include_helpers(base_dirs: List[str]):
  def include_text(path: str) -> str:
    return _resolve_path_for_include(base_dirs, path).read_text(encoding="utf-8")
  def read_file(path: str) -> str: return include_text(path)
  def include_text_glob(pattern: str, sep: str = "\n") -> str:
    pat = expand_path(pattern)
    matches = sorted(glob.glob(pat, recursive=True))
    if not matches:
      for base in base_dirs:
        matches = sorted(glob.glob(str(Path(base) / pattern), recursive=True))
        if matches: break
    if not matches: die(f"include_text_glob found no matches for pattern: {pattern}")
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
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: die(f"Failed to parse JSON include '{path}': {e}")
    return None
  return include_text, read_file, include_text_glob, glob_paths, read_json

def render_template(template_path: Path, context: dict, extra_search: List[str]) -> str:
  ensure_jinja2()
  import jinja2  # type: ignore
  from jinja2 import FileSystemLoader, ChoiceLoader
  base_dir = str(template_path.parent.resolve())
  search_paths = _dedupe_keep_order([base_dir] + [str(Path(p).resolve()) for p in extra_search] + [os.getcwd()])
  loader = ChoiceLoader([FileSystemLoader(search_paths)])
  env = jinja2.Environment(loader=loader, autoescape=False, trim_blocks=True, lstrip_blocks=True)
  register_filters(env)
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

