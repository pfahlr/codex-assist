### Instruction

You are a **senior AI implementation engineer** completing **Phase 3 of a multi-stage Codex synthesis pipeline**.
You favor object oriented solutions and those that implement loosely coupled and highly cohesive design pattens:

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

### Pre-flight Setup (Sandbox Safe Git Setup)
```bash
OWNER={{OWNER}}
REPO={{REPO}} : 
"${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/{{OWNER}}/{{REPO}}.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin;
```

---

### 📤 Post-Execution Output for Phase 4 Handoff

After completing the implementation:

Write post-execution feedback to:

```
codex/agents/POSTEXECUTION/P3/{{CODEX_TASK}}-<unique_identifier_for_this_codex_run>
```

Use the following schema:

```yaml
post_execution_feedback:
  was_successful: true | false
  merged_branch: codex/implement-dsl-policy-engine-in-yaml-<xyz>
  evaluation_notes:
    - description: "All trace events validated; schema conformance passed"
    - description: "enforce() API matches preview plan expectations"
  gaps_identified:
    - id: tool_blocklist_recursion
      description: "Recursion in allowlist resolution not handled in merged branch"
    - id: diagnostics_surface
      description: "`DiagnosticResult` model not preserved"
  suggestions_for_next_phase:
    - Integrate diagnostics model from `reclz1`
    - Reintroduce trace sink middleware from `81p0id`
handoff_contract:
  next_phase_consumer: codex_phase4_synthesizer
  required_schema: codex/specs/schemas/full_task.schema.json
  filter_logic:
    exclude_branch: "<top-ranked-branch>"
    only_include_tasks_adapted_from_nonmerged
```

---

### Final Note

This phase is **live production implementation**.
Think like a peer engineer preparing code for deployment.
