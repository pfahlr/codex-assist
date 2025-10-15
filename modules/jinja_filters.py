from __future__ import annotations

from typing import Any, Callable, Mapping, MutableMapping, Optional, Sequence, TYPE_CHECKING

from .utils import die

try:  # pragma: no cover - import guard
  import yaml  # type: ignore
except Exception:  # pragma: no cover - handled at runtime
  yaml = None  # type: ignore

if TYPE_CHECKING:  # pragma: no cover - typing helper
  from jinja2 import Environment
else:
  Environment = Any  # type: ignore

FilterFunc = Callable[..., Any]

__all__ = ["register_filters", "DEFAULT_FILTERS", "to_nice_yaml", "zip_lists"]


def _require_yaml() -> Any:
  if yaml is None:
    die("YAML support requires PyYAML. Install with: pip install PyYAML")
  return yaml


def to_nice_yaml(value: Any, indent: int = 2) -> str:
  """Render the provided value as a human-friendly YAML string."""
  module = _require_yaml()
  return module.dump(value, default_flow_style=False, sort_keys=False, indent=indent, allow_unicode=True)


def zip_lists(a: Optional[Sequence[Any]], b: Optional[Sequence[Any]]) -> list[tuple[Any, Any]]:
  return list(zip(a or [], b or []))


DEFAULT_FILTERS: Mapping[str, FilterFunc] = {
  "to_nice_yaml": to_nice_yaml,
  "zip": zip_lists,
}


def register_filters(env: Environment, extra_filters: Optional[Mapping[str, FilterFunc]] = None) -> Environment:
  filters: MutableMapping[str, FilterFunc] = dict(DEFAULT_FILTERS)
  if extra_filters:
    filters.update(extra_filters)
  env.filters.update(filters)
  return env
