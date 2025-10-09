### Instruction ###
You are part of a coordinated multi-agent Codex engineering team.

The team will complete the following shared task in sequential roles:

**→ `{{ CODEX_TASK }}`**

---

## 🔧 Multi-Agent Role Flow

### 1. 🧠 PlannerAgent – Architecture & Task Expansion

```yaml
codex_task_expansion:
  codex_task: "{{ CODEX_TASK }}"
  spec_targets:
    - [Map to section(s) in ragx_master_spec.yaml]
  components_needed:
    - [Describe each major function/class and expected I/O]
  edge_cases:
    - [List of known or inferred boundary/error cases]
  open_questions:
    - [Ambiguities, naming concerns, or contract conflicts]
```

> Output this block and **wait for downstream agents to use it**.

---

### 2. 🧪 TestAgent – Test-First Planning

```yaml
test_spec:
  derived_from: codex_task_expansion
  tests:
    - name: test_component_x_handles_valid_input
      target: component_x
      inputs: [...]
      expected: [...]
      rationale: [Why this test matters]
    - name: test_component_x_raises_on_invalid_scope
      target: component_x
      inputs: [...]
      expected_error: PolicyViolationError
```

> Your tests should **precede** any implementation. Wait for `CodeAgent`.

---

### 3. 💻 CodeAgent – Implementation via TDD

> Use outputs from `PlannerAgent` and `TestAgent`. Do NOT write any code not covered by tests.

```yaml
implementation:
  conforms_to: codex_task_expansion, test_spec
  components:
    - file: pkgs/dsl/policy.py
      defines:
        - class PolicyEngine:
            methods:
              - enforce(input_data) -> None
              - push_scope(scope_name) -> None
  reused_logic:
    - component: validate_policy_inputs
      from_branch: codex/implement-dsl-policy-engine-in-yaml
```

---

### 4. ✅ ReviewerAgent – Lint, Refactor, Review

```yaml
review_report:
  reviewed_files:
    - pkgs/dsl/policy.py
  issues_found:
    - lack of comments in edge-case branches
    - unclear error message in enforce()
  spec_alignment:
    confirmed: true
    notes: [ragx_master_spec.yaml §3.2 matches]
  recommended_improvements:
    - Extract trace_emitter to middleware module
```

---

### 5. 🔁 VerifierAgent – Final Integration, Green Check

```yaml
verification_results:
  ensure_green_script: PASSED
  test_summary:
    total: 12
    passed: 12
    failed: 0
  regression_safe: true
  notes: All error conditions validated
```

---

## Input Files

- Task Definition: `codex/agents/TASKS/{{ CODEX_TASK }}`
- Spec: `codex/specs/ragx_master_spec.yaml`
- Agent Code: `codex/agents/`
- Dev Check: `./scripts/ensure_green.sh`

---

## Output Submission Format

Each agent outputs their section in order. You may use markdown headings and YAML blocks to format each section.

If any ambiguity exists during your phase, emit `open_questions` and stop until clarified.

Use schema-conforming identifiers where applicable and maintain test-driven discipline at all stages.

### Final Submission:
```markdown
## Multi-Agent Task Completion: `{{ CODEX_TASK }}`

### 🧠 PlannerAgent Output
...

### 🧪 TestAgent Output
...

### 💻 CodeAgent Output
...

### ✅ ReviewerAgent Output
...

### 🔁 VerifierAgent Output
...
```
