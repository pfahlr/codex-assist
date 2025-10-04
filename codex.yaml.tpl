# Template/include search paths (merged with CLI; CLI has precedence)
template_search:
  - templates
  - shared/partials

# Load structured docs (merged into root context in order)
load:
  - config/base.yaml
  - config/branch.json

# Load docs into specific keys (single -> scalar; many -> list)
load_into:
  DATA: data/*.json
  BUGS:
    - bugs/b1.yaml
    - bugs/b2.yaml

# Provide default CLI-like sets when omitted on the command line
set:
  - owner=pfahlr
  - repo=ragx
set_file:
  - intro=docs/intro.md
add:
  - tasks=Write tests
  - tasks=Fix CI

# Optional default output destination
out: out/prompt.md
