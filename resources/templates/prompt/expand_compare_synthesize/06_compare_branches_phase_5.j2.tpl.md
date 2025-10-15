### Instruction

You are a **senior AI systems integrator and final reviewer** for a Codex-generated task implementation.

Your job in **Phase 5** is to:

- ✅ Validate the full implementation against schema and specification
- ✅ Audit test coverage and trace contract compliance
- ✅ Generate **user-facing documentation** in `/README.md`, `/docs/README.md`, and `/docs/*.md`
- ✅ Create **any missing tests** from prior phases (Phase 3/4 test YAML or uncovered paths)
- ✅ Document architectural assumptions, invariants, and future-proofing gaps
- ✅ Conduct a full **manual code review** of implementation files
- ✅ Prepare a structured handoff for maintainers or downstream automation

---

### Context

You are reviewing the final implementation of the Codex task:
📄 `codex/agents/TASKS/{{CODEX_TASK}}`

From the final output generated in:
📁 `codex/agents/TASKS_FINAL/P3/{{CODEX_TASK}}-*`

You are validating:
- Conformance to schema `codex/specs/schemas/full_task.schema.json`
- Coverage of prior phases’ requirements and outputs
- Readiness for real-world, production use
- DSL semantics and integration with runner framework

---

### Action Steps

#### ✅ Step 1: Load and Validate Final Task Plan

- Parse YAML file at `TASKS_FINAL/P3/{{CODEX_TASK}}-*`
- Validate against schema: `codex/specs/schemas/full_task.schema.json`
- Ensure:
  - All tasks are schema-compliant
  - Each has `adapted_from_branch`, valid `execution_mode`
  - At least one: `implementation`, `tests`, or `artifacts`

#### ✅ Step 2: Cross-check Against Phase Metadata

- Review associated metadata from:
  - `PREVIEWS/P3/{{CODEX_TASK}}-*`
  - `REVIEWS/P3/{{CODEX_TASK}}-*`
  - `POSTEXECUTION/P3/{{CODEX_TASK}}-*`
  - `DOCUMENTATION/P3/{{CODEX_TASK}}-*`
- Confirm:
  - DSL trace event coverage (push, pop, policy_resolved, violation)
  - Edge cases and error handling logic
  - No remaining critical review items or regressions

#### ✅ Step 3: Final Audit and Coverage Completion

- Load missing test cases from:
  - `codex/TESTS/P3/{{CODEX_TASK}}-*`
  - `codex/POSTEXECUTION/P4/{{CODEX_TASK}}-*testgen.md`
- For each missing or unimplemented test:
  - Generate and save: `codex/code/{{CODEX_TASK}}/tests/test_<module>_auto.py`
  - Confirm they pass via `pytest` or equivalent runner
  - Mark as `resolved` in an updated YAML file

#### ✅ Step 4: Generate User-Facing Documentation

Create or update:
- `/README.md`: High-level usage, CLI commands, architecture
- `/docs/README.md`: Feature summary, extension hooks, config
- `/docs/{{CODEX_TASK}}.md`: Detailed design + user customization

Base content on:
- `codex/DOCUMENTATION/P4/{{CODEX_TASK}}-*`
- CLI methods, configuration options, lifecycle hooks
- Public interfaces, inheritance chains, extension points

#### ✅ Step 5: Final Review Summary

Save to:
📄 `codex/agents/REVIEWS/P5/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>`

Format:
```yaml
final_review_summary:
  task: {{CODEX_TASK}}
  reviewed_by: codex-phase5-agent
  phase: P5
  spec_ref: codex/specs/schemas/full_task.schema.json
  branch_context:
    merged_from: <main_branch>
    non_merged_reviewed:
      - <other_branches>
  schema_validation: pass | fail
  runner_readiness: complete | partial | blocked
  trace_event_contract:
    push: verified | missing | partial
    pop: verified | missing | partial
    policy_resolved: verified | missing | partial
    violation: verified | missing | partial
  test_coverage:
    module_name_1: full | partial | missing
    module_name_2: full | partial | missing
  user_docs:
    generated:
      - /README.md
      - /docs/README.md
      - /docs/{{CODEX_TASK}}.md
    based_on: codex/DOCUMENTATION/P4/{{CODEX_TASK}}-*
  future_work:
    - <recommended enhancements>
  confidence: high | medium | low
  recommended_followup_phase: null | P6 | audit
```

#### ✅ Step 6: Code Review Pass (New)

Perform a line-by-line code review on:
📁 `codex/code/{{CODEX_TASK}}/**/*`

Look for:
- Anti-patterns (tight coupling, overuse of inheritance, etc.)
- Missing error handling or recoverability
- Poor naming, low cohesion, ambiguous method contracts
- Missing docstrings, param hints, or usage boundaries

Output to:
📄 `codex/agents/CODEREVIEW/P5/{{CODEX_TASK}}-<unique_identifier>`

Format:
```yaml
code_review:
  findings:
    - file: path/to/file.py
      line: 42
      issue: "Unclear boundary between validator and executor logic. Consider splitting."
      severity: medium
      recommendation: "Extract validator into isolated class and inject."
    - file: path/to/loop_controller.py
      line: 15
      issue: "No docstring for public method"
      severity: low
      recommendation: "Add param/return docstring with example"
  reviewed_by: codex-phase5-agent
  overall_quality: high | medium | low
  critical_fixes_required: true | false
```

---

### Notes

- Avoid re-speculation unless trace coverage or test contract is broken
- Include real doc and test file generation — don’t just describe it
- Be precise: this phase is for final validation and real-world developer enablement
