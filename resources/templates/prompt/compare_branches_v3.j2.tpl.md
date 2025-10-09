### Instruction

You are a **lead AI systems engineer** specializing in **multi-branch code synthesis**, **diff-based reconciliation**, and **Codex task orchestration**.

Your goal is to perform an **expert comparative analysis** of the implementations related to:

```
codex/agents/TASKS/{{CODEX_TASK}}
```

across the following Git branches:

{% for b in BRANCHES %}
* {{ b }}
{% endfor %}

Then, you must synthesize an **actionable, schema-valid YAML development plan** optimized for execution by downstream GPT-5 Codex agents.

---

### Context

This module implements the **DSL Policy Engine** used by the **RAGX DSL runtime** to govern tool access, apply hierarchical policies, and emit deterministic traces.

The unified implementation must preserve:
* Hierarchical “nearest-scope-wins” semantics
* Full trace coverage (`push`, `pop`, `policy_resolved`, `violation`)
* Validation for unknown tools, cycles, and malformed policies
* Runner integration readiness (`enforce()` API, `PolicyViolationError` class)

---

### Role

Act as a **peer senior AI systems engineer** reviewing Codex-generated code.
Use a **precise, implementation-focused, future-proofing tone**.

---

### Action Steps

1. **Repository Setup**
   Establish a sandbox and fetch all branches (see Pre-flight script below).

2. **Code Discovery**
   Identify all files participating in the DSL Policy Engine (`pkgs/dsl/policy.py`, `pkgs/dsl/models.py`, `pkgs/dsl/linter.py`, etc.).

3. **Perform Git Diffs**
   For each branch pair, include:
   - Raw `git diff` excerpts
   - Commentary interpreting logic or design impact

4. **Comparison Matrix**
   Build a structured table (or bullet list) capturing:
   - Unique strengths
   - Common flaws
   - Missing/contradictory logic
   - Architectural and test coverage observations

5. **Synthesize a Unified Architecture**
   Combine best practices from each branch into a cohesive system.

---

### 🧭 Step 6: Synthesis Preview

Before generating the final development plan, produce a `plan_preview` section that includes:

- Logic reused from each branch
- Conflicts and how you'll resolve them
- Open questions or tradeoffs
- Any exclusions or redesign decisions

Wait for confirmation if interactive. Then proceed to YAML.

---

### Step 7: Produce Full Output (Preview, Plan, Metadata)

#### Output A: Review Summary

```yaml
metadata:
  last_updated: {{ TODAY }}
  repo: {{OWNER}}/{{REPO_NAME}}
  tags: [dsl, codex_task, policy_engine, traceability, refactor]
  execution_mode: plan_synthesis  # or plan_validation
analysis:
  branch_diffs:
    - from: codex/implement-dsl-policy-engine-in-yaml
      to: codex/implement-dsl-policy-engine-in-yaml-yp01n0
      git_diff: |
        [Git diff block]
      commentary: |
        [Code-level design interpretation]
  summary_of_findings:
    common_flaws:
      - Missing “policy_resolved” trace
    unique_strengths:
      - reclz1 has extensible policy model
    critical_gaps:
      - yp01n0 misapplies scope push logic
confidence_notes:
  - area: enforce() semantics
    confidence: medium
    reason: divergent behavior across branches
coverage_gaps:
  - missing: unit test for `policy_resolved` trace
  - missing: recursion validation in allowlist expansion
traceability_checklist:
  - must-emit: push
  - must-emit: pop
  - must-emit: policy_resolved
  - must-raise: PolicyViolationError
```

---

#### Output B: Unified Codex Task Plan

```yaml
plan_preview:
  branch_inclusions:
    - codex/...-reclz1: diagnostics and structured metadata
    - codex/...-81p0id: event trace contract
  conflict_resolution:
    - normalize enforce() to exception-based path
  exclusions:
    - remove allowlist entry fallback logic
  open_questions:
    - Should traces emit to file or callback?

refinement_opportunities:
  - Refactor PolicyStack into stateful components
  - Replace hardcoded tag-checks with validator plugins

shared_blocks:
  - name: scope_enforcer
    implementation: |
      def enforce_scope_resolution(stack, tool):
          ...
  - name: trace_event_emitter
    implementation: |
      def emit_trace_event(event_type, context):
          ...

tasks:
  - id: setup_policy_core
    execution_mode: always
    reusable: true
    description: >
      Establish validated PolicyStack with deterministic scope resolution and error-checking.
    source_files:
      - pkgs/dsl/policy.py
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml
    implementation_ref: scope_enforcer

  - id: integrate_diagnostics_layer
    execution_mode: always
    reusable: true
    description: Add ToolDescriptor and diagnostics metadata.
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml-reclz1
    dependencies: [setup_policy_core]
    source_files:
      - pkgs/dsl/models.py
      - pkgs/dsl/policy.py
    implementation:
      python: |
        @dataclass(frozen=True)
        class ToolDescriptor:
            name: str
            tags: tuple[str, ...]

  - id: add_policy_enforce_api
    execution_mode: always
    reusable: false
    description: Enforce tool access and emit structured trace events.
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml-yp01n0
    dependencies: [integrate_diagnostics_layer]
    source_files:
      - pkgs/dsl/policy.py
    tests:
      - name: test_blocked_tool_raises
        file: tests/unit/test_policy_enforce.py

  - id: finalize_tracing_contract
    execution_mode: optional
    reusable: true
    description: Emit all DSL lifecycle events via PolicyEvent schema.
    adapted_from_branch: codex/implement-dsl-policy-engine-in-yaml-81p0id
    dependencies: [add_policy_enforce_api]
    source_files:
      - pkgs/dsl/policy.py
    implementation_ref: trace_event_emitter
    artifacts:
      - name: policy_event_schema
        file: codex/specs/schemas/policy_trace_event.schema.json
```

---

#### Output C: Post-Execution Feedback (for downstream agents)

```yaml
post_execution_feedback:
  was_successful: null
  failed_tasks: []
  recommended_revisions: []
```

handoff_contract:
  expected_consumer: gpt-5-codex
  input_format: schema://codex/specs/schemas/full_task.schema.json
  output_type: executable-python+unit-tests

codex_directives:
  must:
    - attribute reused logic to specific branches
    - emit `policy_resolved` trace
  do_not:
    - invent tools or APIs not seen in diffs
    - reuse test logic without attribution
```

---

### Pre-flight Git Setup

```bash
OWNER={{OWNER}}
REPO={{REPO_NAME}}
: "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/${OWNER}/${REPO}.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin;

mkdir diffs;
{% for b in BRANCHES %}
git diff {{b}} > diffs/{{b}}.diff
{% endfor %}
```
