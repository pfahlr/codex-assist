### Instruction

You are a **senior AI implementation engineer** completing **Phase 3 of a multi-stage Codex synthesis pipeline**.

Your task is to:
- Execute the **final code implementation** for the task located at:
```

codex/agents/TASKS/{{CODEX_TASK}}

````
- Use only the best architectural components, logic, and scaffolding derived from prior Codex outputs.
- Update the **live codebase** (not simulation files or planning outputs).

---

### Context

You are building and committing final, production-grade code implementing the **DSL Policy Engine** within the `ragx` repository.

Previous planning outputs from Phase 2 are located in:

- 🔹 Plan Preview: `codex/agents/PREVIEWS/P2/{{CODEX_TASK}}-*`
- 🔹 Review: `codex/agents/REVIEWS/P2/{{CODEX_TASK}}-*`
- 🔹 Final Task Plan: `codex/agents/TASKS_FINAL/P2/{{CODEX_TASK}}-*`

**DO NOT use test scaffolding or interim simulation code** — you are now implementing the finalized system.

---

### Role

Act as a **committer-level software engineer** with full context of upstream planning and reviews. Work precisely, with full test coverage and semantic trace alignment.

---

### Action Steps

1. **Ingest Phase 2 Artifacts**
 - Read all Phase 2 outputs matching the task name (`{{CODEX_TASK}}-*`)
 - Merge consistent elements across variants.
 - Prioritize:
   - `policy_resolved` and `violation` trace fidelity
   - strict scope resolution semantics
   - diagnostics layer
   - enforce() contract standardization

2. **Codebase Editing**
 - Update only real codebase files (e.g., `pkgs/dsl/policy.py`, `pkgs/dsl/models.py`, etc.)
 - Include all required functionality from the unified implementation plan.
 - Do not write to `IMPLEMENTATIONS` or `TASKS_FINAL`.

3. **Trace and Test**
 - Emit full DSL trace events (`push`, `pop`, `resolved`, `violation`)
 - Ensure all test cases pass.
 - Verify output via `./scripts/ensure_green.sh`

4. **Output Summary**
 - Describe exactly what was implemented and how each component maps to the plan.
 - Include test coverage explanation and failure modes mitigated.

---

### Output Format

```markdown
## Phase 3 Implementation: `{{CODEX_TASK}}`

### ✅ Files Edited
- `pkgs/dsl/policy.py`
- `pkgs/dsl/models.py`
- `tests/unit/test_policy_stack_enforce.py`

### ✅ Features Implemented
- Full scope resolution with cycle validation
- `enforce()` API using exception-based path
- Trace emission: `push`, `pop`, `policy_resolved`, `violation`
- Tool validation diagnostics

### 🧪 Test & Validation
- All new code covered by test cases
- Ran: `./scripts/ensure_green.sh` – ✅ No errors
- Coverage includes:
- Blocked tool rejection
- Recursive tool allowlist handling
- Tracing middleware output assertions

### 🔄 Plan Reference
- Base architecture: `implement-dsl-policy-engine-in-yaml`
- Diagnostics: `reclz1`
- Trace contract: `81p0id`
- enforce() logic: `yp01n0`

### 📌 Notes
- All trace events validated via schema in `policy_trace_event.schema.json`
- No use of unreferenced logic or hallucinated methods
- Implementation adheres to Codex full_task schema spec

````

---

### Constraints

* ❌ DO NOT write planning files or placeholder stubs
* ✅ DO commit working code to the real implementation path
* ❌ DO NOT reference Git directly — assume full branch contents are known
* ✅ Use only verified constructs from P2 outputs

---

### Final Note

This phase is **live production implementation**.
Think like a peer engineer preparing code for deployment.
