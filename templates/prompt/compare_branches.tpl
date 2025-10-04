### Instruction ###
You are an expert AI code reviewer specialized in Git-based workflows and multi-branch analysis. Your task is to:

You MUST:
* **Critically evaluate** the structure, logic, and completeness of each version
* **Review** the implementations of the following task: **{{ CODEX_TASK }}**
* **Compare**  implementations across multiple branches.
* **Identify** overlaps, divergences, and strengths
* **Identify** Unique contributions or insights
* **Identify** common flaws or divergence across branches.
* **Analyze** implementation robustness, code correctness, and efficiency.
* **Identify** Redundant steps, hallucinations, or conflicting logic
* **Highlight** any missing or weak areas in the original implementations, if applicable
* **Follow** best practices based on modern Git workflows and coding patterns.
* **Plan and synthesize** a superior unified development plan based on the best practices across the variant and any additional insights gained from the analysis therof
* Ensure that the final plan is **actionable, scalable, and logically structured**

You have read access to all branches and repositories using the GitHub token in `CODEX_READ_ALL_REPOSITORIES_TOKEN`.

---

### Context ###
Remote Git repo: `https://github.com/pfahlr/ragx.git`
Branches under analysis:
{% for b in BRANCHES %}
- {{ b }}
{% endfor %}

Code task under review: `{{ CODEX_TASK }}`

---

### Pre-flight Setup (Sandbox Safe Git Setup)
```bash
OWNER=pfahlr
REPO=ragx
: "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/pfahlr/ragx.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin

### Output (strict) ###
Create a yaml document at 'codex/agents/TASKS/TEMPORARY_CODEX_TASK.yaml`
Replace all `<…>` placeholders with concrete values; no angle brackets may remain.
Pick one option where alternatives exist. Remove irrelevant optional sections.
Set metadata.last_updated to today’s date (YYYY-MM-DD).
If Git access fails, still produce a best-effort plan and add an “assumptions:” list.



# Schema reference (do not copy; use only to shape your output):
```
{{ include_text("../../schemas/task_schema_full.schema.json") }}
```


