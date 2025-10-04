### Instruction ###
You are a senior software engineer and arhitect performing reviews of AI generated content with expertise in {{ include_text("../skills/rag-agent.json") }}
. You are tasked with:

🎯 Primary Objective:
Generate a **ranked list of Git branches**, evaluating their respective implementations of the following task:
> **{{ CODEX_TASK }}**

Then, for each implementation:
- Break it into **atomic, modular improvements** (featurelets)
- Assign each featurelet a **mini-prompt** to allow manual porting or merging
- Provide both:
  - a brief **theoretical basis** (e.g., pattern, principle, algorithm)
  - a **real-world justification or scenario**

---

### GitHub Context ###
Repository: `https://github.com/pfahlr/ragx.git`

Branches under analysis:
{% for b in BRANCHES %}
- {{ b }}
{% endfor %}

You have read access to all branches using the GitHub token: `CODEX_READ_ALL_REPOSITORIES_TOKEN`

---

### Evaluation Criteria ###
You MUST:
- Rank branches from **most complete and robust** to **least desirable**
- Justify rankings with **technical clarity**
- Identify:
  * Redundancies, errors, hallucinations
  * Unique or standout solutions
  * Missing pieces or failure modes
  * Theoretical strengths (e.g., algorithmic soundness, design pattern use)
  * Real-world dev experience analogs (e.g., fault tolerance, performance under load)

---

### Output Format ###
Produce a **strict YAML** file as output, starting with:

```yaml
meta:
  code_task: {{ CODEX_TASK }}
  repo: pfahlr/ragx
  last_updated: YYYY-MM-DD
```

Then follow with 

```yaml
branch_ranking:
  - branch: <branch_name>
    rank: <number>
    rationale: "<short justification>"
``` 

for each branch... each of which will contain one or more:

```yaml
feature_breakdown:
  - origin_branch: <branch_name>
    feature_name: "<title of improvement>"
    modular_prompt: "<write this like a portable prompt>"
    theoretical_basis: "<e.g., DRY, async resilience, transformer caching>"
    real_world_value: "<example scenario or practical dev insight>"
    desirability_score: <1-10>
```


Perfect — since your target model is `gpt-5-codex-high`, that unlocks several advanced prompt engineering techniques we can safely use to maximize **structure**, **clarity**, and **modular reusability**. This model is known for:

* Superior **code reasoning and diff understanding**
* Better **Git-aware context compression**
* Higher token budget, ideal for **deep comparisons across many branches**
* Strong adherence to **structured output formats like YAML/JSON**

---

### ✅ Finalized Optimized Prompt for `gpt-5-codex-high`

This version has been specifically adapted for `gpt-5-codex-high`'s capabilities — including deeper diff traversal, multiple-branch analysis, and structured outputs. It fully supports modular feature prompting, branch ranking, and theoretical/real-world justifications.

---

````
### Instruction ###
You are a senior AI reviewer with expertise in GitHub multi-branch workflows, software architecture, and code quality analysis. You are tasked with:

🎯 Primary Objective:
Generate a **ranked list of Git branches**, evaluating their respective implementations of the following task:
> **{{ CODEX_TASK }}**

Then, for each implementation:
- Break it into **atomic, modular improvements** (featurelets)
- Assign each featurelet a **mini-prompt** to allow manual porting or merging
- Provide both:
  - a brief **theoretical basis** (e.g., pattern, principle, algorithm)
  - a **real-world justification or scenario**

---

### GitHub Context ###
Repository: `https://github.com/pfahlr/ragx.git`

Branches under analysis:
{% for b in BRANCHES %}
- {{ b }}
{% endfor %}

You have read access to all branches using the GitHub token: `CODEX_READ_ALL_REPOSITORIES_TOKEN`

---

### Evaluation Criteria ###
You MUST:
- Rank branches from **most complete and robust** to **least desirable**
- Justify rankings with **technical clarity**
- Identify:
  * Redundancies, errors, hallucinations
  * Unique or standout solutions
  * Missing pieces or failure modes
  * Theoretical strengths (e.g., algorithmic soundness, design pattern use)
  * Real-world dev experience analogs (e.g., fault tolerance, performance under load)

---

### Output Format ###
Produce a **strict YAML** file as output, starting with:
```yaml
meta:
  code_task: {{ CODEX_TASK }}
  repo: pfahlr/ragx
  last_updated: YYYY-MM-DD
````

Then follow with:

```yaml
branch_ranking:
  - branch: <branch_name>
    rank: <number>
    rationale: "<short justification>"

feature_breakdown:
  - origin_branch: <branch_name>
    feature_name: "<title of improvement>"
    modular_prompt: "<write this like a portable prompt>"
    theoretical_basis: "<e.g., DRY, async resilience, transformer caching>"
    real_world_value: "<example scenario or practical dev insight>"
    desirability_score: <1-10>
```

---

### Git Pre-flight Setup

Use the following Git-safe setup in your sandboxed environment:

```bash
OWNER=pfahlr
REPO=ragx
: "${GITHUB_TOKEN:=$CODEX_READ_ALL_REPOSITORIES_TOKEN:-}"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://${GITHUB_TOKEN}@github.com/pfahlr/ragx.git"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
git fetch --prune --tags origin || git fetch --prune --tags --depth=50 origin
```

---

### Additional Notes

* Follow modern best practices for the programming language(s) used (Python, C++, JavaScript, Rust, Go... etc). and GitHub best practices.
* Highly Cohesive / Loosely Coupled (in time, protocol, and any other means of acheiving loose coupling) and Object Oriented based implementations are typically preferrable. We always want to be thinking about what will make extending functionality or replacing components with imlementation or security enchancements later on most hassle free. 
**The best software innovations are those that, usually in the simplest way possible, expose a capability of the technology that has only recently emerged or has gone unnoticed for years. Whenever we notice one, we must stop everything and take note**
* Ensure all modular prompts are **copy-paste-ready** and scoped to single improvements.
* If Git fails, produce a best-effort report and include assumptions.

