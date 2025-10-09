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

write the review to `codex/agents/REVIEWS/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>`

---

### 🧭 Step Prompting Phase: Synthesis Preview

Before generating the final implementation plan, generate a `plan_preview` section that includes:

* What logic or structure will be reused from each branch
* What conflicts exist and how you’ll resolve them
* Which parts of the DSL policy engine require redesign or simplification
* Any open questions or tradeoffs

write the plan preview to the file `codex/agents/PREVIEWS/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>`

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

write the final implementation plan to `codex/agents/TASKS_FINAL/P2/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>`

---

### Example Plan Format

```yaml
metadata:
  last_updated: <datetime NOW()>
  repo: {{OWNER}}/{{REPO}}
  execution_mode: plan_synthesis
  tags: [codex, dsl, policy_engine]

plan_preview:
  branch_inclusions:
    - codex/...-reclz1: diagnostic modeling
    - codex/...-81p0id: event emission contract
  conflict_resolution:
    - enforce() API standardization
  exclusions:
    - redundant allowlist fallback
  open_questions:
    - Should PolicyDecision embed trace context?

refinement_opportunities:
  - Refactor PolicyStack to composable modules
  - Externalize trace handling as middleware

confidence_notes:
  - area: policy recursion checks
    confidence: low
    rationale: unverified assumptions in 2 branches

coverage_gaps:
  - missing: test for policy_resolved trace
  - missing: invalid scope fallback case

traceability_checklist:
  - must-emit: push
  - must-emit: pop
  - must-emit: policy_resolved
  - must-raise: PolicyViolationError

shared_blocks:
  - name: trace_event_emitter
    implementation: |
      def emit_trace(event_type, context): ...

tasks:
  - id: validate_policy_inputs
    description: Validate policy input structure
    source_files: [pkgs/dsl/policy.py]
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml
    execution_mode: always
    reusable: true
    implementation:
      python: |
        class PolicyDefinitionError(ValueError): ...

  - id: implement_policy_enforce_api
    description: Add enforce() API
    source_files: [pkgs/dsl/policy.py]
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml-yp01n0
    depends_on: [validate_policy_inputs]
    execution_mode: always
    reusable: false
    tests:
      - test_enforce_blocks_tools

  - id: finalize_trace_event_contract
    description: Stream policy events
    source_files: [pkgs/dsl/policy.py]
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml-81p0id
    execution_mode: optional
    reusable: true
    implementation_ref: trace_event_emitter
    artifacts:
      - name: policy_event_schema
        file: codex/specs/schemas/policy_trace_event.schema.json

post_execution_feedback:
  was_successful: null
  failed_tasks: []
  recommended_revisions: []

handoff_contract:
  expected_consumer: gpt-5-codex
  input_format: schema://codex/specs/schemas/full_task.schema.json
  output_type: executable-python+unit-tests

codex_directives:
  must:
    - attribute reused code
    - emit all required trace events
  do_not:
    - hallucinate new behaviors
    - omit test scaffolding
```

---

### Input Data

You are reviewing the following guideline drafts:

{% for i in IMPLEMENTS %}
Variation {{ loop.index }}:
```yaml
{{ i }}
```
{% endfor %}

---

### Context

Repo: `https://github.com/{{OWNER}}/{{REPO}}.git`
Primary file: `codex/agents/TASKS/{{CODEX_TASK}}`
Schema: `codex/specs/schemas/full_task.schema.json`

---

### Pre-flight Git Setup

```bash
OWNER={{OWNER}}
REPO={{REPO}}
: "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/${{OWNER}}/${{REPO}}.git"
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
