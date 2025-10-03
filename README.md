```asciiart
╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ ╔═══════════════════════════════════════════════╗ ┊
┊ ║                                               ║ ┊
┊ ║  ███████████████████████████████████████████  ║ ┊
┊ ║  █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█  ║ ┊
┊ ║  █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█  ║ ┊
┊ ║  █▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓█  ║ ┊
┊ ║  █▓░                                     ░▓█  ║ ┊
┊ ║  █▓░  ┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ╔═══════════════════════════╗ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║                           ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║                           ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║   𜷡𜴂𜴅𜴀𜷥🮂𜶘𜵈𜶘𜵊𜶚▖𜶘𜷂𜵇▘𜴦𜶻𜵫▘    ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║   𜴅𜴫𜴯𜴀𜴦𜴧𜴱▘𜴱𜴬𜴖𜺨𜴱𜴬𜴨🯦𜴵𜺨𜴢🯦    ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║                           ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║  ███████████████████████  ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║  █▌▄▐█ ■▄█ ■▄█ █ ■▄█▄ ▄█  ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║  █ ▄ █▀■ █▀■ █ █▀■ ██ ██  ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║  ███████████████████████  ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ║                           ║ ┊  ░▓█  ║ ┊
┊ ║  █▓░  ┊ ╚═══════════════════════════╝ ┊  ░▓█  ║ ┊
┊ ║  █▓░  └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘  ░▓█  ║ ┊
┊ ║  █▓░                                     ░▓█  ║ ┊
┊ ║  █▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓█  ║ ┊
┊ ║  █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█  ║ ┊
┊ ║  █▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█  ║ ┊
┊ ║  ███████████████████████████████████████████  ║ ┊
┊ ║                                               ║ ┊
┊ ╚═══════════════════════════════════════════════╝ ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯
```


# Codex Assistant

A tiny, fast utility to render **Jinja2** templates into finished prompts, PR comments, scripts, and docs — all from the command line — with strong support for arrays, nested keys, JSON, and file/glob inputs. First tool in the **Codex Assistant** toolkit: `codex_prompt_builder.py`.

---

## Why this exists

Because prompts that generate code are a form of code themselves. A well structured prompt that initiates a coding task producing a desired result can be reused 
with slight modifications. This is why I've built this program to perform string replacement on tokens in prompts that I will use over and over again. 

Please, take a look around. If nothing else, reviewing the code in this repository might provide you with useful insight into a different way of looking at the process of using AI to generate software. 

### YAML as Specifications

If you want to communicate specifications for software between LLM models, yaml is an excellent serialized data format for the job. 

When asking an LLM to generate specifications, you can provide a yaml template that outlines the necessary components to define. 

Here's an incomplete example:

```yaml
version: <number>
id: <master_task_id>
title: <string>
summary: >
  <high-level summary of the overall effort (Parts A+B)>
description: >
  <narrative describing the overall goal, constraints, and how the two-part flow works>
metadata:
  owners: [ "you@example.com" ]
  labels: [ "tests-first", "impl", "observability", "mcp" ]
  priority: P1
  risk: medium
  last_updated: "<YYYY-MM-DD>"
  links:
    - { type: "design_doc", url: "<url>" }
    - { type: "tracking_issue", url: "<url>" }
  tickets: [ "<JIRA-1234>" ]
scope:
  goals:
    - <goal 1>
    - <goal 2>
assumptions:
  - <assumption 1>
component_ids: [ <string>, <string> ]
depends_on: [ <string> ]
arg_spec: [ <string> ]
observability_requirements:
    - Keep logging/scheming minimal, only as needed for assertions.
    - Deterministic seeds and stable sorting for reproducible fixtures.
server_contract:
    transports:
    http:
        framework: fastapi
        endpoints:
        - { method: GET,  path: /mcp/discover,          response: envelope }
        - { method: GET,  path: /mcp/prompt/{promptId}, response: envelope }
        - { method: POST, path: /mcp/tool/{toolId},     response: envelope }
        - { method: GET,  path: /healthz,               response: { status: ok } }
        shutdown: graceful
    cli_contract:
    program: <cli_command>
    commands:
    - name: build
        flags:
        - { name: --input, type: path, required: true }
        - { name: --output, type: path, required: true }
        exit_codes:
        - { code: 0, meaning: ok }
        - { code: 2, meaning: invalid input }
structured_logging_contract:
    format: jsonl
    storage_path_prefix: runs/<area>/<task>
    retention: keep-last-5
    event_fields: *log_event_fields
    metadata_fields: [ runId, attemptId, schemaVersion, deterministic ]
    volatile_fields: *volatile_fields
log_diff_strategy:
    tool: deepdiff.DeepDiff
    baseline_path: tests/fixtures/<area>/<task>_golden.jsonl
    whitelist_fields: *volatile_fields
artifacts:
    tests:
    unit:
        - tests/unit/<module>/test_<topic>_spec.py
        - tests/unit/<module>/test_<topic>_errors.py
    integration:
        - tests/integration/<topic>/test_round_trip_spec.py
    property_based: []
    fixtures:
    - tests/fixtures/<area>/<task>_golden.jsonl
    - tests/fixtures/<area>/<name>.json
    stubs:
    - src/<pkg>/<module>.py
    schemas:
    - apps/schemas/<name>.schema.json
    docs:
    - docs/<area>/<task>_spec.md
test_matrix:
    python: [ "3.11" ]
    os: [ "ubuntu-latest" ]
test_plan:
    unit:
    - tests/unit/<module>/test_<topic>_spec.py
    integration:
    - tests/integration/<topic>/test_round_trip_spec.py
    property_based:
    - tests/property/test_<topic>_contracts.py
    fixtures:
    - tests/fixtures/<area>/<task>_golden.jsonl
```
you can probably see how much information about specific implementation details it is possible to represent in this way. 

One trick to enhance an LLMs ability to write code that you might not guess straight away is to 1) generate several variations on the same request. 2) have another LLM analyze the varations on the implementation and produce a yaml outline of a final implementation integrating the parts of each of the variants that work best. You can then generate an implementation based on this outline. *You might even consider watching what happens when you repeat the process with the refined yaml task.*

I have prompts for this very procedure in the templates directory. 

---

## Features

* **Any template file**: `--template-name path/to/template.tpl`
* **Simple tokens**: `--set KEY=VALUE` (supports `@file` shorthand)
* **JSON tokens**: `--set-json KEY='<json>'` and `--set-json-file KEY=path.json`
* **Arrays without brackets (zsh-friendly)**

  * Append scalars/files: `--add KEY=VALUE`, `--add-file KEY='snips/*.md'`
  * Set by index: `--set-index KEY:2=VALUE`, `--set-file-index KEY:2=path.txt`
* **Scalar or list from files/globs**: `--set-file KEY='notes/*.txt'`
  (1 match → string, many → list of strings)
* **Nested keys via dot notation**: `PARENT.CHILD=value`
* **File shorthand**: `--set KEY=@path/to/file.txt` (use `@@` to escape a literal `@`)
* **Built-in `zip` filter** for parallel iteration in templates
* **Debug view**: `--print-context` prints the final JSON context

> Still compatible with `KEY[]` / `KEY[2]` forms for Bash users, but you no longer need brackets (which zsh can mangle).

---

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install Jinja2
# add your preferred runner alias
alias codex-prompt='python codex_prompt_builder.py'
```

Requires Python **3.8+**.

---

## Quick start

1. Create a template `templates/hello.tpl`:

```jinja2
Hello {{ USER }}!

You have {{ TASKS|length }} task(s):
{% for t in TASKS %}
- {{ loop.index }}. {{ t }}
{% endfor %}
```

2. Render it:

```bash
python codex_prompt_builder.py \
  --template-name templates/hello.tpl \
  --set USER=Rick \
  --add TASKS='Write tests' \
  --add TASKS='Fix CI' \
  --out hello.txt
```

Result (`hello.txt`):

```
Hello Rick!

You have 2 task(s):
- 1. Write tests
- 2. Fix CI
```

---

## CLI overview

### Core flags

* `--template-name PATH` — Jinja2 template to render
* `--out PATH` — where to write output (stdout if omitted)
* `--print-context` — dump the merged context (JSON) to stderr

### Setting tokens

* **Scalars**: `--set KEY=VALUE`

  * `VALUE` may be `@file.txt` to inline a file’s UTF-8 contents
  * Use `@@` to escape a literal `@` (e.g., `@@headline` → `@headline`)
* **JSON**:

  * `--set-json KEY='<json>'`
  * `--set-json-file KEY=path.json`

### Arrays (zsh-friendly forms)

* **Append**:

  * `--add KEY=VALUE`
  * `--add-file KEY='snips/*.md'` (appends contents of each match)
* **Set by index**:

  * `--set-index KEY:2=VALUE`
  * `--set-file-index KEY:2=path.txt` (exactly one file must match)

### Scalar OR list from files/globs

* `--set-file KEY='notes/*.txt'`

  * 1 match → `KEY` is a string
  * > 1 match → `KEY` becomes a list of strings (sorted lexicographically)

> **Tip (zsh & bash)**: **Quote** globs (`'notes/*.txt'`) so the script can perform deterministic sorting and handle errors nicely.

---

## Nesting & data model

* Dotted keys create objects:
  `--set REPO.owner=pfahlr --set REPO.name=ragx` →

  ```json
  { "REPO": { "owner": "pfahlr", "name": "ragx" } }
  ```
* Arrays live at any level:
  `--add BUGS='Null ref' --add BUGS='Off-by-one'` →

  ```json
  { "BUGS": ["Null ref", "Off-by-one"] }
  ```

---

## Examples

### 1) Branch list + bug table from files

```bash
python codex_prompt_builder.py \
  --template-name templates/codex_review.tpl \
  --set OWNER=pfahlr \
  --set REPO=ragx \
  --set TOKEN_ENVVAR=CODEX_READ_ALL_REPOSITORIES_TOKEN \
  --set-file BRANCHES='branches/*.txt' \
  --add-file BUG_TEXTS='bugs/*.md' \
  --out prompt.txt
```

### 2) Parallel iteration with `zip`

Template snippet:

```jinja2
{% for bid, btxt in BUG_IDS|zip(BUG_TEXTS) %}
- {{ bid }}: {{ btxt }}
{% endfor %}
```

Command:

```bash
python codex_prompt_builder.py \
  --template-name templates/bugs.tpl \
  --add BUG_IDS=B1 --add BUG_TEXTS='Crash on startup' \
  --add BUG_IDS=B2 --add BUG_TEXTS='CI cache miss on PR' \
  --out bugs.txt
```

### 3) Mixed nested JSON + arrays

```bash
python codex_prompt_builder.py \
  --template-name templates/plan.tpl \
  --set-json META='{"owner":"pfahlr","project":"Codex Assistant"}' \
  --add TASKS='Spec review' \
  --add-file TASKS='tasks/*.md' \
  --set-index TASKS:0='Kickoff' \
  --out plan.txt
```

---

## Templating tips

* **Whitespace control**: Jinja2 supports `trim_blocks` and `lstrip_blocks` (enabled here) for clean output.
* **Conditionals**:

  ```jinja2
  {% if NOTES %}Notes: {{ NOTES|length }} item(s){% endif %}
  ```
* **Safety**: Auto-escape is **off** (we’re rendering plain text). Escape manually if you output into HTML/Markdown and need sanitization.

---

## Behavior & edge cases

* **Encoding**: Files are read as **UTF-8**.
* **Globs**: Sorted lexicographically. Quote them to avoid shell expansion.
* **Indexing**: `--set-file-index` requires **exactly one** file match.
* **Overrides**: Later flags can override earlier scalar keys; appends extend lists.
* **Exit codes**: Non-zero on invalid flags, missing files, bad JSON, or template not found.

---

## Security notes

* Treat `@file` and `--set-file` inputs as untrusted content if they come from outside your repo.
* Templates can execute logic; keep them simple and reviewed in PRs.

---

## Project layout (suggested)

```
codex-assistant/
├─ codex_prompt_builder.py
├─ templates/
│  ├─ hello.tpl
│  ├─ codex_review.tpl
├─ examples/
│  ├─ branches/
│  │  ├─ fix-1.txt
│  │  └─ fix-2.txt
│  └─ bugs/
│     ├─ B1.md
│     └─ B2.md
└─ README.md
```


