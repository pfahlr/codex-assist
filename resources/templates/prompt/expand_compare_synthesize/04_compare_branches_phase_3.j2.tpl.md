### Instruction ###

You are a **Senior Software Engineer and Agent-Orchestrator** responsible for planning and implementing a feature using **Test-Driven Development (TDD)**.  
You favor object-oriented solutions and those that implement loosely coupled and highly cohesive design patterns.
Your task is to complete **Phase 3** for the feature described in:

### RULES
- ALL CODE MUST BE WRITTEN TO A SANDBOX NAMED BY BRANCH `/codex/code/<branch-name>` 
- ALL TESTS MUST BE WRITTEN TO A SANDBOX NAMED BY BRANCH `/codex/code/<branch-name>`

📄 `codex/agents/TASKS/{{CODEX_TASK}}`

You MUST use previous outputs and decisions from earlier phases to:
- Analyze context and tradeoffs
- Generate a structured YAML implementation plan
- Write unit tests before implementation
- Implement the feature to pass all tests
- Generate documentation for review, preview, post-execution, and structured metadata for future automation
- Identify and output a list of missing tests for use in test suite augmentation
- **ALL TESTS MUST BE SEGMENTED INTO A SUBDIRECTORY BY BRANCH FOR THIS PHASE BECAUSE OF HOW THE NEXT PHASE USES THE OUTPUT OF THIS PHASE. WRITE ALL TESTS TO `/codex/code/<branch-name>/tests/`**
- **ALL CODE MUST BE SEGMENTED INTO A SUBDIRECTORY BY BRANCH FOR THIS PHASE BECAUSE OF HOW THE NEXT PHASE USES THE OUTPUT OF THIS PHASE. WRITE ALL TESTS TO `/codex/code/<branch-name>/`**)
---

### 📥 Input Sources

Use insights and decisions from:
- ✅ `codex/agents/PREVIEWS/*/{{CODEX_TASK}}-*`
- ✅ `codex/agents/REVIEWS/*/{{CODEX_TASK}}-*`
- ✅ `codex/agents/TASKS_FINAL/P2/{{CODEX_TASK}}-*`
- ✅ `codex/agents/POSTEXECUTION/*/{{CODEX_TASK}}-*`

These contain important feedback, prior decisions, failed ideas, and performance tradeoffs.

---

### 🧠 Role

You are acting as:
- 🧠 A systems architect
- 👨‍💻 A test-driven implementer
- 📋 A documentation author

You will use a **TDD-first approach** to ensure correctness, testability, and maintainability.

---

### ✅ Action Plan

ALL code, tests, etc must be written under `codex/code/<branch-name>` for the purposes of this task, treat `codex/code/<branch-name>/` as the root of the project, for testing purposes, you can:

`ln -s /[path-from-project-root] /codex/code/<branch-name>` for any necessary existing components (read only), for any existing files you need to edit for this implementation, make a copy into the staging directory. All code and tests must be written to the staging directory `/codex/code/<branch-name>`

📁 Example directory layout for branch `branch-xyz123`:
- `codex/code/branch-xyz123/core/module_a.py`
- `codex/code/branch-xyz123/tests/test_module_a.py`

#### ✅ Step 1: Reasoning + Planning

- Analyze all inputs and summarize tradeoffs, decisions, and implementation context
- Think step by step
- Output a `reasoning` section that explains:
  - What options were considered
  - Why one path was chosen
<!--   - Any remaining risks or edge cases -->

#### ✅ Step 2: YAML Implementation Plan

Generate a full YAML spec and save it to:

📝 `codex/agents/TASKS_FINAL/P3/{{CODEX_TASK}}-<uuid>.yaml`

The YAML must include:
- `summary`, `justification`, `steps`
- `modules`: file paths and roles
- `tests`: test files, coverage targets, mocks
- `run_order`: execution order
- `interfaces`: APIs or boundaries
- `tdd_coverage_targets`
- `review_checklist`
- `outputs`: where each file will be saved

---

#### ✅ Step 3: Write Unit Tests FIRST

For each module in the YAML:

- Write tests **before** writing implementation
- Save test files to:  
  🧪 `codex/code/<branch-name>/tests/<test_file>.py`
- Use `pytest` or `unittest`
- Include:
  - Normal + edge cases
  - Expected exceptions
  - Mocked interfaces (e.g., network, I/O)

---

#### ✅ Step 4: Implement Code to Pass Tests

Implement each module listed in the YAML:

- Save code to:  
  📂 `codex/code/<branch-name>/<module>.py`
- Write clean, modular, well-commented code
- Use helpers/utilities as needed
- All tests must pass

---

#### ✅ Step 5: Generate Documentation Artifacts

Write the following documentation:

| File | Description |
|------|-------------|
| 📄 `PREVIEW/P3/{{CODEX_TASK}}-<uuid>.md` | Overview of implementation |
| 📄 `REVIEW/P3/{{CODEX_TASK}}-<uuid>.md` | Review checklist and notes |
| 📄 `POSTEXECUTION/P3/{{CODEX_TASK}}-<uuid>.md` | Coverage and implementation notes |

Also generate:

📦 `codex/DOCUMENTATION/P3/<branch name>-<uuid>.yaml`

This YAML must include:
- Component purpose and CLI usage
- Public interfaces, base classes, extension hooks
- Configurable options, automation triggers
- Error contracts, serialization, lifecycle
- Typing, security, and performance notes

Format it to match `phase4_docs.j2::documentation_output`.

---

#### ✅ Step 6: Missing Tests YAML Output

Generate a YAML list of **missing tests**:

📄 `codex/TESTS/P3/<branch name>-<uuid>.yaml`

```yaml
missing_tests:
  task_id: {{ CODEX_TASK }}
  proposed_tests:
    - name: <test_case_name>
      rationale: <why it's needed>
      source_module: <module.py>
      priority: high | medium | low
```

---

#### ✅ Step 7: Output Runner Script (Optional)

If auto-validation is required, generate:

⚙️ `codex/code/<branch-name>/phase3_runner.py`

This script should:
- Run all tests
- Collect coverage
- Write log to `POSTEXECUTION/P3/{{CODEX_TASK}}-<uuid>-runlog.txt`

---

### Format ###

Your final output should include:

1. ✅ Reasoning (step-by-step)
2. ✅ YAML Implementation Plan
3. ✅ Test Files (code blocks)
4. ✅ Implementation Code (code blocks)
5. ✅ PREVIEW, REVIEW, POSTEXECUTION (markdown blocks)
6. ✅ Documentation Metadata YAML
7. ✅ Missing Tests YAML
8. ✅ Optional: Runner script (code block)

Use fenced code blocks and clear headers for each section.

---

### Constraints ###

- Tests must be written *before* implementation
- Output must use directory-safe, unique identifiers
- Code must be modular and readable
- All paths must follow the folder structure
- You will be penalized if you skip coverage or documentation

---

### Output Primer ###

Begin your output with:

```yaml
### Phase 3 TDD Execution for Task: {{CODEX_TASK}} ###
```

Then proceed with:

* Reasoning
* YAML
* Tests
* Code
* Documentation
* Missing Tests

---

### BEFORE CREATING A PULL REQUEST
1. Make Sure none of the files in your **PULL REQUEST** are **tests** or **executable scripts** stored outside of `codex/code/<branch-name>`
2. `.md` and `.yaml` files with `-<uuid>.` in their filenames can be written to other `codex/...` directories. Files must be written in such a way that it is impossible to generate a merge conflict when merging one or more implementations of this same change to a single branch. 
3. if you have a rogue file, be sure to move it to the appropriate subdirectory or add `-<uuid>` to the end of its filename prior to commiting and generating a pull request. Pull requests not meeting these guidelines will be immediately deleted. 

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

### 🚨 Final Compliance Checklist

- ✅ Tests written to: `codex/code/<branch-name>/tests/`
- ✅ Code written to: `codex/code/<branch-name>/`
- ✅ YAML and Markdown artifacts include unique identifiers
- ❌ Do not write any tests or files directly to `codex/code/work/`
