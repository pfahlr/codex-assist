from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .utils import die, expand_path
from .structload import load_structured_file

LOCAL_NAMES = ["codex.yaml", "codex.yml", "codex.json"]


def _user_config_candidates() -> List[Path]:
  home = Path.home()
  candidates: List[Path] = []
  # Linux (XDG)
  xdg = os.getenv("XDG_CONFIG_HOME", str(home / ".config"))
  candidates += [Path(xdg) / "codex-assistant" / n for n in ["config.yaml","config.yml","config.json"]]
  # macOS
  candidates += [home / "Library" / "Application Support" / "Codex Assistant" / n
                 for n in ["config.yaml","config.yml","config.json"]]
  # Windows
  appdata = os.getenv("APPDATA")
  if appdata:
    candidates += [Path(appdata) / "Codex Assistant" / n
                   for n in ["config.yaml","config.yml","config.json"]]
  return candidates


def find_config_path(explicit: Optional[str]) -> Optional[Path]:
  if explicit:
    p = Path(expand_path(explicit)).resolve()
    if p.exists():
      return p
    die(f"--config path not found: {p}")
  # local first
  for name in LOCAL_NAMES:
    p = (Path(name)).resolve()
    if p.exists():
      return p
  # user-level
  for p in _user_config_candidates():
    if p.exists():
      return p.resolve()
  return None


def load_config(path: Path) -> Dict[str, Any]:
  docs = load_structured_file(str(path))
  doc = docs[0] if docs else {}
  if not isinstance(doc, dict):
    die(f"Config must be a mapping at top level: {path}")
  return doc


def env_tpl_paths() -> List[str]:
  val = os.getenv("CODEX_TPL_PATH")
  if not val:
    return []
  sep = ";" if os.name == "nt" else ":"
  return [p for p in val.split(sep) if p]


def merge_config_into_args(args_ns, cfg: Dict[str, Any], base_dir: Path) -> None:
  """Mutate argparse namespace by filling defaults from config.
  CLI flags (if provided) already have values; we only extend defaults.
  Paths in the config are resolved relative to the config file directory.
  """
  import os as _os

  def _join_if_relative(p: str) -> str:
    p = expand_path(p)
    return p if _os.path.isabs(p) else str((base_dir / p).resolve())

  def _rewrite_pairs_rhs(pairs: List[str]) -> List[str]:
    out: List[str] = []
    for pair in pairs:
      if "=" not in pair:
        die(f"Invalid pair (missing '='): {pair}")
      k, v = pair.split("=", 1)
      out.append(f"{k}={_join_if_relative(v)}")
    return out

  def _strip_index_prefix(s: str) -> str:
    if "=" not in s:
      return s
    parts = s.split("=")
    if parts and parts[0].isdigit():
      return "=".join(parts[1:])
    return s

  # flags to fill from config when CLI didn't supply them
  for key, dest in [
    ("template_search", "template_search"),
    ("load", "load"),
    ("load_into", "load_into"),
    ("set", "set"),
    ("set_json", "set_json"),
    ("set_json_file", "set_json_file"),
    ("set_file", "set_file"),
    ("add", "add"),
    ("add_file", "add_file"),
    ("set_index", "set_index"),
    ("set_file_index", "set_file_index"),
  ]:
    if key in cfg and getattr(args_ns, dest, None) == []:
      val = cfg[key]
      if isinstance(val, list):
        if dest in ("template_search",):
          setattr(args_ns, dest, [_join_if_relative(x) for x in val])
        elif dest in ("load",):
          cleaned: List[str] = []
          for x in val:
            s = _strip_index_prefix(str(x))
            cleaned.append(_join_if_relative(s))
          setattr(args_ns, dest, cleaned)
          setattr(args_ns, "_load_optional", True)           # mark as optional (from config)
        elif dest in ("load_into",):
          pairs: List[str] = []
          for item in val:
            if isinstance(item, dict):
              for k, v in item.items():
                pairs.append(f"{k}={_join_if_relative(v)}")
            else:
              s = _strip_index_prefix(str(item))
              if "=" in s:
                k, v = s.split("=", 1)
                pairs.append(f"{k}={_join_if_relative(v)}")
              else:
                pairs.append(_join_if_relative(s))  # path-only; CLI will validate if used
          setattr(args_ns, dest, pairs)
          setattr(args_ns, "_load_into_optional", True)      # mark as optional (from config)
        elif dest in ("set_file", "add_file", "set_json_file", "set_file_index"):
          setattr(args_ns, dest, _rewrite_pairs_rhs(list(val)))
        else:
          setattr(args_ns, dest, list(val))
      elif isinstance(val, dict) and dest == "load_into":
        pairs = []
        for k, v in val.items():
          if isinstance(v, list):
            pairs += [f"{k}={_join_if_relative(item)}" for item in v]
          else:
            pairs.append(f"{k}={_join_if_relative(v)}")
        setattr(args_ns, dest, pairs)
        setattr(args_ns, "_load_into_optional", True)        # mark as optional (from config)
      else:
        if dest in ("template_search",):
          setattr(args_ns, dest, [_join_if_relative(val)])
        elif dest in ("load",):
          s = _strip_index_prefix(str(val))
          setattr(args_ns, dest, [_join_if_relative(s)])
          setattr(args_ns, "_load_optional", True)           # mark as optional (from config)
        elif dest in ("set_file", "add_file", "set_json_file", "set_file_index"):
          setattr(args_ns, dest, _rewrite_pairs_rhs([val] if isinstance(val, str) else list(val)))
        else:
          setattr(args_ns, dest, [val])

  # Optional default output path
  if "out" in cfg and getattr(args_ns, "out", None) in (None, ""):
    setattr(args_ns, "out", cfg["out"])

  # Fold in env CODEX_TPL_PATH if present and not already added
  env_paths = env_tpl_paths()
  if env_paths:
    current = getattr(args_ns, "template_search", [])
    setattr(args_ns, "template_search", current + env_paths)
