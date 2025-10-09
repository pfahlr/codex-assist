### Instruction

You are a senior AI systems engineer collaborating with Codex. Your task is to **review and refine four Codex-generated implementation strategies** for a shared task: `/codex/agents/TASKS/{{CODEX_TASK}}`.

Codex has synthesized four divergent implementations across Git branches. You MUST:

---

### Section A: Comparative Technical Review (per CRAFT)

**Act as an expert peer reviewer. For each version:**

* Use bullet points under each branch label (e.g. `Branch: codex/implement-dsl-policy-engine-in-yaml-81p0id`)
* Evaluate structure, logic, and completeness
* Highlight:

  * Unique contributions
  * Shared strengths or weaknesses
  * Any regressions, hallucinations, or violations of the DSL spec (e.g. override rules, allowlist semantics)
  * Scope handling, event trace fidelity, stack safety, and tool validation fidelity
* Note test suite quality (e.g. missing decision/loop tests, scope-check enforcement)

Also include:

* **Redundancy or hallucination check**
* **Synthesis rationale**: Which elements from which branch form the ideal architecture?
* **Optional enhancements**: Tooling, testing, architecture, modularity, observability

Write the review to:
```plaintext
codex/agents/REVIEWS/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>
```

---

### 🧭 Step Prompting Phase: Synthesis Preview

Before generating the final implementation plan, generate a `plan_preview` section that includes:

* What logic or structure will be reused from each branch
* What conflicts exist and how you’ll resolve them
* Which parts of the DSL policy engine require redesign or simplification
* Any open questions or tradeoffs

Write the preview to:
```plaintext
codex/agents/PREVIEWS/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>
```

Wait for confirmation if interactive. Then continue.

---

### Section B: Final Implementation Plan (Schema-Valid, Modular)

Your output MUST be:

* Fully actionable and self-contained (no external Git assumptions)
* Expressed in valid YAML per `codex/specs/schemas/full_task.schema.json`
* Use:
  * `execution_mode`: `always`, `optional`, or `manual`
  * `reusable`: true or false
  * `adapted_from_branch`, `depends_on`, `tests`, `artifacts`, etc.

Write the plan to:
```plaintext
codex/agents/TASKS_FINAL/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>
```

---

### Post-Execution Summary

After synthesizing the implementation plan:

Write a `post_execution_feedback` block to:

```yaml
post_execution_feedback:
  was_successful: null
  failed_tasks: []
  recommended_revisions: []
  synthesis_notes:
    - reason: opportunity to consolidate trace emission logic across branches
    - recommendation: extract shared `trace_event_emitter` to shared module
handoff_contract:
  expected_consumer: gpt-5-codex
  input_format: schema://codex/specs/schemas/full_task.schema.json
  output_type: executable-python+unit-tests

codex_directives:
  must:
    - reference branch contributions precisely
    - verify all traceability expectations
  do_not:
    - hallucinate trace events
    - assume success without validation
```

Write this to:

```
codex/agents/POSTEXECUTION/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>
```
---


### Pre-flight Setup (Sandbox Safe Git Setup)
```bash
OWNER={{OWNER}}
REPO={{REPO}} : 
"${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/{{OWNER}}/{{REPO_NAME}}.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin;

{% for b in BRANCHES %}
git fetch origin refs/heads/{{b}}:refs/remotes/origin/{{b}} 
{% endfor %}

mkdir diffs;

{% for b in BRANCHES %}
git diff {{b}} > diffs/{{b}}.diff
{% endfor %}
```

### Input Data Discovery

Use the following as input:

```python
import glob
IMPLEMENT_FILES = glob.glob('codex/agents/TASKS_VARIANTS/P1/{{CODEX_TASK}}-*')
```

Then loop over and load each variation file for analysis.

---



### Context

Repo: `https://github.com/{{OWNER}}/{{REPO}}.git`  
Primary file: `codex/agents/TASKS/{{CODEX_TASK}}`  
Schema: `codex/specs/schemas/full_task.schema.json`

---


