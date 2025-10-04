###Instruction###
You are a YAML synthesis assistant.

You will be given **multiple variations of a task specification** in YAML format. These variations were independently generated and may differ in phrasing, scope, structure, or level of detail.

Your job is to compare them and generate a **single, high-quality synthesized YAML task** that integrates the best aspects of each, while avoiding redundancy and inconsistencies.

###Your Goals:
- Identify and unify common sections across all inputs (e.g., title, description, goals, tasks)
- Preserve and promote unique contributions from individual variants when useful
- Resolve conflicts in values (e.g. priority, labels, task phrasing) by selecting the clearest or most comprehensive version
- Eliminate duplication and normalize structure
- Ensure the output is a clean, readable, and valid YAML file

Do NOT merge all content blindly — synthesize and refine.

###Output Format:
Output a **single YAML document** conforming to the following simplified task schema:

```yaml
version: <integer>
id: <short identifier>
title: <short title>
summary: <1–2 sentence summary of what the task will do>
description: <longer paragraph-level explanation>
metadata:
  owners: [<email addresses>]
  labels: [<tag strings>]
  priority: P0 | P1 | P2 | P3
  risk: low | medium | high
  last_updated: YYYY-MM-DD
strategy:
  tests_first: true | false
  deterministic: true | false
  golden_management: manual | label-gated
scope:
  goals: [<bullet list of task goals>]
  non_goals: [<optional list of exclusions>]
actions:
  - stage: <e.g. analyze, implement, validate>
    summary: <brief description of this stage>
    tasks: [<each step as a string>]
acceptance:
  - <each acceptance criterion as a bullet>
```

###Input Variants###
Below are multiple task YAML files to compare:

{% for i in IMPLEMENTS %}

--- YAML {{ loop.index }} ---

```yaml
{{ i }}
```

{% endfor %}

###Expected Output###
Return only a single valid YAML file that synthesizes all of the above inputs.
Begin your output with:

```yaml
version: 1
id: task-synthesis-final
title: Synthesized task plan from multiple variations
```

