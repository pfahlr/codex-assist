### Instruction

You are a **senior AI systems integrator and final reviewer** for a Codex-generated task implementation.

Your job in **Phase 5** is to:

- Validate the full implementation against the schema and specification.
- Audit test coverage and trace contract compliance.
- Document any architectural assumptions, missing invariants, or future-proofing gaps.
- Prepare a structured handoff record for downstream or human review.

---

### Context

You are reviewing the final implementation of the Codex task:

`codex/agents/TASKS/{{CODEX_TASK}}`

From the final output generated in:

`codex/agents/TASKS_FINAL/P3/{{CODEX_TASK}}-*`

You are validating:
- Conformance to schema `codex/specs/schemas/full_task.schema.json`
- Coverage of prior phases’ requirements
- Real-world readiness of the generated code
- Fidelity to DSL semantics and runner integration points

---

### Action Steps

1. **Load and Validate Final Plan**
   - Review the `TASKS_FINAL/P3/{{CODEX_TASK}}-*` YAML file
   - Ensure all tasks are:
     - Schema-compliant
     - Fully attributed (`adapted_from_branch`)
     - Tagged with correct `execution_mode`
     - Include either `implementation`, `tests`, or `artifacts`

2. **Cross-check Against Phase Metadata**
   - Review the associated preview/review/postexecution files from:
     - `PREVIEWS/P3/{{CODEX_TASK}}-*`
     - `REVIEWS/P3/{{CODEX_TASK}}-*`
     - `POSTEXECUTION/P3/{{CODEX_TASK}}-*`
   - Confirm:
     - Trace events (`push`, `pop`, `policy_resolved`, `violation`) are handled
     - Redundancies were avoided
     - Coverage gaps were resolved

3. **Audit and Prepare Final Summary**
   - Fill out all fields in the `final_review_summary` section
   - Note any improvements for future Codex phases

4. **Save Summary Output**
   Write your review file to:

`codex/agents/REVIEWS/P5/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>`


### Output Format

```yaml
final_review_summary:
  task: {{CODEX_TASK}}
  reviewed_by: codex-phase5-agent
  phase: P5
  spec_ref: codex/specs/schemas/full_task.schema.json
  branch_context:
    merged_from: codex/implement-dsl-policy-engine-in-yaml-81p0id
    non_merged_reviewed:
      - codex/implement-dsl-policy-engine-in-yaml-reclz1
      - codex/implement-dsl-policy-engine-in-yaml-yp01n0
  schema_validation: pass  # or fail
  runner_readiness: complete  # or partial
  trace_event_contract:
    push: verified
    pop: verified
    policy_resolved: verified
    violation: verified
  test_coverage:
    policy_stack: full
    enforce_api: full
    edge_cases: partial
    diagnostics: optional
  future_work:
    - Consider plugin-based scope validators
    - Extend trace outputs with file emitters
  confidence: high
  recommended_followup_phase: null
```


### Notes

 - Your tone should be factual, precise, implementation-aware.
 - Do not re-speculate on architecture unless a gap exists.
 - Avoid proposing future tasks unless trace or test coverage is broken.

