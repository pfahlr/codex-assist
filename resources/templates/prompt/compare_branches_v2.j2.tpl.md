{#
Template Variables:

- CODEX_TASK (`05_yada_yada.yaml`)
- BRANCHES[] (codex/yada_yada , codex/yada_yada-o349ds, ...)
- REPO_NAME ('ragx' for https://github.com/pfahlr/ragx.git)

#}
### Instruction ###
You are an expert AI code reviewer specialized in **multi-branch Git analysis**, **diff-based diagnostics**, and **robust code synthesis**. You favor object oriented solutions and those that are highly cohesive and loosely coupled.

Your task is to deeply analyze and compare the **actual code implementations** related to the task `codex/agents/TASKS/{{CODEX_TASK}}` across the following Git branches:

{% for b in BRANCHES %}
- {{ b }}
{% endfor %}

---

### Step-by-Step Instructions ###
1. **Repository Setup**
   Set up a Git sandbox with access using `CODEX_READ_ALL_REPOSITORIES_TOKEN`, and fetch all remote branches and tags.

2. **Code File Identification**
   Go beyond the task YAML. Locate **all code files** implementing or interacting with the DSL policy engine in each branch.

3. **Perform Git Diffs**
   Use `git diff` to identify meaningful differences in logic, structure, and semantics between branches. For each comparison, include:
   - Actual `git diff` blocks (not just summaries)
   - Commentary explaining significance of each change
   - Any detected anti-patterns or best-practice violations

4. **Comparison Matrix**
   Build a structured comparison of:
   - Unique contributions per branch
   - Overlapping patterns
   - Redundant code or logic
   - Missing or hallucinated logic
   - Performance, maintainability, and correctness issues

5. **Important Elements to Note**
   - Unique contributions or insights
   - Common flaws or divergence across branches
   - Hallucinations, Redundant steps, conflicting logic
   - Missing or weak areas in each branch

6. **Analysis Framework**
   - Giving consideration to all the information gathered in the 4. Comparison Matrix and 5. Important Elements to Note determine:
   - implementation robustness
   - code correctness
   - code efficiency
   - code extensibility
   - code maintainability
   - is the code highly cohesive?
   - is the code loosely coupled?

6. **YAML ↔ Code Coverage Check**
   Confirm whether the YAML specification is fully supported by the code in each branch. Flag incomplete or over-engineered sections.

7. **Synthesize a Unified Implementation Strategy**
   Based on the best parts of each branch, define a **scalable, maintainable, and efficient plan** to implement the DSL policy engine.

---

### Output Format (Strict YAML + Code Diff Format) ###

Produce two artifacts:

#### 1. Structured YAML File
Path: `TEMPORARY_CODEX_TASK.yaml`

```yaml
metadata:
  last_updated: 2025-10-09
assumptions:
  - All Git branches were accessible and fetched correctly
analysis:
  branch_diffs:
    - from: <branch 1>
      to: <branch 2>
      git_diff: |
        [Insert git diff block here]
      commentary: |
        [Explain the implications of the diff: changes in flow, data structure, logic, etc.]
  summary_of_findings:
    common_flaws: [...]
    unique_strengths: [...]
    critical_gaps: [...]
unified_plan:
  strategy: |
    [Step-by-step plan to combine strengths into a single clean implementation]
```

#### 2. Git Diffs (Inline or Separate Code Blocks)

Embed inline git diff blocks with annotations to make the review concrete, e.g.:
```
diff --git a/policy_engine.py b/policy_engine.py
index 12ab345..67cd890 100644
--- a/policy_engine.py
+++ b/policy_engine.py
@@ def evaluate_policy(self, input_data):
-    if input_data['role'] == 'admin':
-        return True
+    if input_data.get('role') == 'admin':
+        return self.allow_all()
     return False
```

### Directives

- You *MUST* prioritize **code-level differences**, not just YAML.
- You *MUST* embed actual `git diff` blocks in output.
- You *MUST* offer critical commentary and synthesis.
- Ensure all output is technically actionable and unbiased.
- You will be penalized for shallow or YAML-only responses.

### Context ###
Repo: `https://github.com/pfahlr/{{REPO_NAME}}.git`
Primary task file: {{CODEX_TASK}}
All supporting code files across branches must be considered.
---

### Pre-flight Setup (Sandbox Safe Git Setup)
```bash
OWNER=pfahlr
REPO={{REPO_NAME}}
: "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/pfahlr/{{REPO_NAME}}.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin;

mkdir diffs;

# Helper shell to collect and store diffs
{% for b in BRANCHES %}
git diff {{b}} > diffs/{{b}}.diff
{% endfor %}
```

### Output (strict) ###
Create a yaml document at '/TEMPORARY_CODEX_TASK.yaml`
Replace all `<…>` placeholders with concrete values; no angle brackets may remain.
Pick one option where alternatives exist. Remove irrelevant optional sections.
Set metadata.last_updated to today’s date (YYYY-MM-DD).
If Git access fails, still produce a best-effort plan and add an “assumptions:” list.


# Schema reference (do not copy; use only to shape your output):
see file
`codex/specs/schemas/full_task.schema.json`

`cat codex/specs/schemas/full_task.schema.json`

```
{{ include_text("../../schemas/task_schema_full.schema.json") }}
```

