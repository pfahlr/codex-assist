###Instruction###
You are an advanced Git-aware code review assistant working in a sandbox environment.

You’ve been provided with these Codex-generated branches which attempt to improve AVS rendering diagnostics and frame capture:

{% for b in BRANCHES %}
- {{b}}
{% endfor %}

These branches have NOT been merged.

Each branch attempts to:

{{ TASK_DESCRIPTION }}

The main branch already has one implementation merged. Your job is to:
- Compare the three unmerged branches against the current code
- Extract any useful, unique, or improved diagnostics, capture logic, or logging
- Recommend which changes to adopt
- Output a **single YAML task plan** (ragx_task.yaml) that summarizes the implementation strategy for incorporating those improvements

###Output Requirement###
Produce a valid **YAML file** that conforms to the following simplified schema:

```yaml
version: <integer>
id: <short identifier>
title: <short title>
summary: <1-2 sentence summary of what the task will do>
description: <longer, paragraph-level explanation>
metadata:
  owners: ["pfahlr@gmail.com"]
  labels: [<tag strings>]
  priority: P0 | P1 | P2 | P3
  risk: low | medium | high
  last_updated: YYYY-MM-DD
strategy:
  tests_first: true | false
  deterministic: true | false
  golden_management: manual | label-gated
scope:
  goals: [<bullet list of goals>]
  non_goals: [<optional bullet list of exclusions>]
actions:
  - stage: <e.g. analyze, merge, refactor>
    summary: <description of the stage>
    tasks: [<each task as a bullet>]
acceptance:
  - <each acceptance criterion as a bullet>

store it in the root of the project as `./TEMPORARY_TASK_YAML.YAML'
