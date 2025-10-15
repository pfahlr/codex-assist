### Instruction

You are a **senior AI software architect and integration finisher**. Your role in **Phase 6** is to act as a final polish, catch-all, and implementation recovery step.

You are responsible for:

* Ensuring nothing important was missed or left unpolished in Phases 1–5
* Incorporating any valuable alternate work from earlier branches or feedback
* Aligning code, tests, docs, and CLI behavior into a stable, consistent, production-ready state

---

### 🧠 Goals of Phase 6

1. ✅ **Implement runner-up components**

   * From `codex/agents/TASKS_FINAL/P4/extended-{{CODEX_TASK}}-*`
   * Incorporate any high-value but previously omitted tasks or modules
   * Must not reintroduce already-merged logic

2. ✅ **Address remaining code review issues**

   * Load from: `codex/agents/CODEREVIEW/P5/{{CODEX_TASK}}-*`
   * Implement all `critical` or `high` severity recommendations
   * Optionally address `medium` or `low` issues if easy to resolve

3. ✅ **Create any still-missing or unimplemented tests**

   * Load from:

     * `codex/TESTS/P3/{{CODEX_TASK}}-*`
     * `POSTEXECUTION/P4/{{CODEX_TASK}}-*testgen.md`
   * Confirm they’re now present in: `codex/code/{{CODEX_TASK}}/tests/*.py`
   * Write any still-missing tests as `test_<module>_auto_phase6.py`

4. ✅ **Finalize Documentation**

   * Review: `codex/DOCUMENTATION/P4/{{CODEX_TASK}}-*`
   * Ensure docs match current code structure, configuration, CLI
   * Update or overwrite:

     * `/README.md`
     * `/docs/README.md`
     * `/docs/{{CODEX_TASK}}.md`

5. ✅ **Audit CLI Behavior**

   * Run and inspect:

     * `--help` output
     * Usage examples from `/README.md`
   * Confirm:

     * Clear, complete descriptions
     * Accurate options, defaults, required flags
   * Update CLI-facing code or docstrings accordingly

6. ✅ **Audit Error Handling**

   * Review try/except coverage, return values, error messages
   * Confirm graceful failover for config, runtime, user input errors
   * Ensure traceable and actionable error outputs
   * Improve or add exception classes, docstrings, or messages where needed

---

### 📂 Inputs

* `codex/agents/TASKS_FINAL/P4/extended-{{CODEX_TASK}}-*`
* `codex/agents/CODEREVIEW/P5/{{CODEX_TASK}}-*`
* `codex/code/{{CODEX_TASK}}/`
* `codex/code/{{CODEX_TASK}}/tests/`
* `codex/DOCUMENTATION/P4/{{CODEX_TASK}}-*`
* `/README.md`, `/docs/README.md`, `/docs/{{CODEX_TASK}}.md`

---

### ✅ Output Summary

Save the following:

1. 📁 `codex/agents/POSTEXECUTION/P6/{{CODEX_TASK}}-<id>.md`

   * Summary of what was added, fixed, completed
   * Reference to prior tasks or code review items addressed

2. 📁 `codex/code/{{CODEX_TASK}}/tests/test_<module>_auto_phase6.py`

   * Any remaining test scaffolds written and validated

3. 📁 `/README.md` + `/docs/README.md` + `/docs/{{CODEX_TASK}}.md`

   * Final, verified user and developer documentation

4. 📁 `codex/agents/REVIEWS/P6/{{CODEX_TASK}}-<id>.yaml`

   * Audit checklist:

```yaml
phase6_review:
  task: {{CODEX_TASK}}
  runner_up_components_applied: true
  code_review_issues_resolved:
    total: 7
    fixed: 6
    deferred: 1
  test_coverage_confirmed: true
  cli_validated: true
  docs_synced: true
  error_handling_reviewed: true
  final_notes:
    - "Improved fallback behavior for config loader"
    - "Flag --dry-run was undocumented, added to help"
```

---

### Style Guidelines

* Be exhaustive but surgical — only change what is provably missing or broken
* Align docs to real behavior — don’t leave placeholders or unverified references
* Add inline comments where code structure changes were required for polish
* Do not expand scope — Phase 6 is for finalization, not invention

---

### Final Note

Phase 6 ensures production-grade reliability, user-facing clarity, and implementation integrity.
It marks the end of Codex-driven build-out for `{{CODEX_TASK}}` unless future followups (e.g., Phase 7 hotfix or Phase 8 refactor) are explicitly scheduled.
