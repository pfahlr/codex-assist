You are a senior managing developer. Review candidate branches, compare their fixes for the listed bugs, design the best consolidated solution, and implement it on a new branch derived from the branch under review (NOT main).

PRE-FLIGHT (robust Git in sandbox)
1) Ensure remote and token:
  OWNER={{ OWNER }}
  REPO={{ REPO }}
  # Map your repo-wide token into GITHUB_TOKEN for HTTPS fetches
  : "${GITHUB_TOKEN:=${{{ TOKEN_ENVVAR }}}:-}"

  # Add origin if missing (HTTPS using token)
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/{{ OWNER }}/{{ REPO }}.git"

  # Fetch all branches and PR heads
  git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
  git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"

  # Fetch (works for shallow/full clones)
  git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin

2) Fetch candidate branches by refspec (sandbox-safe):
{% for b in BRANCHES %}
  git fetch origin refs/heads/{{ b }}:refs/remotes/origin/{{ b }}
{% endfor %}

3) Determine the current review branch (the branch this PR is targeting). Do NOT assume "main".
  # If available from the CI env, prefer it; otherwise detect from git metadata.
  # Use that as the base for the consolidated work.

CREATE WORKING BRANCH
4) From the review branch (checked out), create a working branch:
  BASE=$(git rev-parse --abbrev-ref HEAD)
  git checkout -b codex/consolidated-fix-"$(git rev-parse --short HEAD)"

PROBLEMS TO SOLVE
{% for bug in BUGS %}
- [{{ bug.id }}] {{ bug.text }}
{% endfor %}

ANALYSIS
5) For each remote branch:
  - Inspect diffs (git diff ${BASE}...origin/<candidate>) and identify how each bug is addressed.
  - Note strengths/weaknesses: correctness, readability, maintainability, convention alignment.

CONSOLIDATED DESIGN
6) Plan the unified solution drawing from the best ideas across candidates. Keep it minimal, explicit, and aligned with project conventions.

IMPLEMENTATION
7) Apply the consolidated changes on the working branch.
8) Update tests, docs, and CI as needed.
9) Run formatting, linters, and tests:
  ruff check . || true
  mypy . || true
  pytest -q || pytest --maxfail=1 -q

COMMIT
10) Commit with a clear message:
  git add -A
  git commit -m "Consolidate fixes for bugs: {% for bug in BUGS %}{{ bug.id }}{% if not loop.last %}, {% endif %}{% endfor %} (see description)."

PUSH & PR
11) Push the working branch and open a PR against the current review branch (NOT main). Include a summary with:
  - Table of candidate approaches vs. bugs
  - Rationale for chosen consolidation
  - Notes on CI/build impact and rollback plan

OUTPUT
- A pushed branch codex/consolidated-fix-<shortsha> with the implemented solution.
- A short summary comment explaining which ideas were taken from each candidate and why.
