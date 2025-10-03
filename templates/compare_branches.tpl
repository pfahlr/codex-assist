PRE-FLIGHT (robust Git in sandbox)
1) Ensure remote and token:
  OWNER=pfahlr
  REPO=ragx
  : "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/pfahlr/ragx.git"
  git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
  git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
  git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin

2) Fetch candidate branches by refspec (sandbox-safe):


{% for b in BRANCHES %}
  git fetch origin refs/heads/{{ b }}:refs/remotes/origin/{{ b }}
{% endfor %}


review the implementations of:

codex/agents/TASKS/06ab_core_tools_minimal_subset.yaml

in branches: 
{% for b in BRANCHES %}
{{ b }}
{% endfor %}


you have access to the github token in the secret CODEX_READ_ALL_REPOSITORIES_TOKEN which will give you read access to all repositories and branches within 

analyze the differences between the implementations. determine which elements represent the most robust and effective code implementations, and using what you've learned plan an implementation that combines the best characteristics from the four branches you reviewed. 
