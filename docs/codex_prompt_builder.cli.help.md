Codex Template Builder — Extended Help
======================================

Overview
--------
Render Jinja2 templates using values from CLI flags and/or JSON/YAML config files.
Supports arrays, nested keys, file/glob inputs, and in-template includes.

Typical usage:
  python codex_template_builder.py \
    --template-name templates/prompt.tpl \
    --load config/base.yaml \
    --set owner=pfahlr --add tasks='Write tests' \
    --out out.txt

CLI flags (summary)
-------------------
--template-name PATH
--template-search DIR            # add lookup paths for {% include %} and helpers

--load PATH_OR_GLOB              # parse .json/.yaml/.yml; deep-merge mappings into root
--load-into KEY=PATH_OR_GLOB     # assign parsed doc(s) to KEY (scalar if one; list if many)

--set KEY=VALUE                  # scalar; VALUE may be '@file' (use @@ to escape '@')
--set-json KEY='<json>'
--set-json-file KEY=path.json

--set-file KEY='path/or/glob'    # 1 match -> scalar; many -> list (file contents)
--add KEY=VALUE                  # append scalar (or '@file') to list
--add-file KEY='glob/*.txt'      # append matched file contents to list
--set-index KEY:2=VALUE          # set list element (VALUE may be '@file')
--set-file-index KEY:2=path.txt  # set list element from a single file

--print-context                  # print final JSON context to stderr
--out PATH                       # write render to file (stdout if omitted)

--help-extended                  # show this extended help and exit

Configuration file format (JSON/YAML)
-------------------------------------
You can load structured config via:
  --load config/app.yaml
  --load-into DATA=inputs/*.json

Accepted document types:
  * Mapping (object/dict)  — recommended for --load (deep-merged into root)
  * Any JSON/YAML type     — allowed for --load-into (assigned to KEY)
  * Multi-document YAML    — each doc is loaded; see rules below

Merging rules:
  * --load: Each mapping document is deep-merged into the root context.
            Later files override earlier keys; nested dicts are merged.
  * --load-into KEY=...:
      - 1 file/doc -> KEY is that single value
      - many files/docs -> KEY is a list of those values (in lexicographic order)

Text tokens in config (scalar vs array)
---------------------------------------
As plain JSON/YAML, you can provide scalars, lists, and nested dicts:

YAML:
  owner: pfahlr
  tasks:
    - "Write tests"
    - "Fix CI"
  meta:
    repo: ragx
    branch: main

JSON:
  { "owner": "pfahlr", "tasks": ["Write tests", "Fix CI"], "meta": { "repo": "ragx" } }

File tokens in config (scalar vs array)
---------------------------------------
Use the following **macros** inside JSON/YAML to inline file contents:

  {"$file": "path/to/file.txt"}
      -> Replaced with the UTF-8 text of that file (scalar string)

  {"$files": ["a.txt", "b.txt"]}
      -> Replaced with a list of file texts (array of strings)

  {"$glob": "snips/*.md"}
      -> Replaced with a list of texts for all matching files (sorted lexicographically)

  {"$glob_one": "docs/intro.md"}
      -> Replaced with a single string; errors unless exactly one file matches

Optional:
  {"$glob": "snips/*.md", "$join": "\n\n---\n\n"}
      -> Joins all matched file texts with the given separator (produces a scalar string)

Examples:
  YAML (scalar file token):
    intro: { $file: docs/intro.md }

  YAML (array of files):
    snippets: { $glob: "snips/*.md" }

  YAML (joined into one big string):
    body: { $glob: "sections/*.md", $join: "\n\n" }

  YAML (explicit list of files):
    notes: { $files: ["n1.txt", "n2.txt"] }

Notes:
  * Paths support ~ and $VARS; globs are sorted lexicographically.
  * For --load (root merge), the resolved document must be a mapping (dict).
    If your top-level is a list or scalar, use --load-into KEY=...

Templates — includes & helpers
------------------------------
Native includes:
  {% include "partials/header.tpl" %}

Helpers (available as template globals):
  {{ include_text("docs/intro.md") }}
  {{ include_text_glob("snips/*.md", sep="\n\n") }}
  {% for p in glob_paths("snips/*.md") %}{{ include_text(p) }}{% endfor %}
  {{ read_json("data/spec.json").title }}

Tips
----
* Quote globs in the shell ('snips/*.md') for determinism and clear errors.
* Autoescape is OFF (rendering plain text). Escape as needed for HTML.