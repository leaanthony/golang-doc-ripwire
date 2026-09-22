# Go Documentation with Ripwire

A Go documentation skill that uses source code, caller usage, and executable examples to support its claims. Ripwire helps find relevant code, repetitive comments, and stale Markdown references; Go tooling remains authoritative for package inventory, type checking, and example execution.

## What changed from upstream

- Evidence gathering before writing, with explicit treatment of intended contracts and observed behavior.
- Optional Ripwire recipes for comment review, documentation drift, examples, and architecture explanations.
- Go-specific limitations: graph results are incomplete, `--lego` cannot be assumed to extract Go method sets, and test reachability does not prove execution.
- Mixed library/CLI classification, scoped audits, shared context for large tasks, and fallback when Ripwire is unavailable.
- Concise comments, verified links and claims, completion checks, and behavioral evaluation fixtures.

## Install

Clone this repository into a skill directory recognized by your agent. For Codex's default skill location:

```sh
git clone https://github.com/leaanthony/golang-doc-ripwire.git ~/.codex/skills/golang-doc-ripwire
```

If that directory already exists, update the existing checkout instead of cloning over it. Agents using a custom skill home should use that location. The skill lives at the repository root; no other skills are required. Go is needed for Go checks. Ripwire is optional and must already be available to use its recipes.

Invoke `golang-doc-ripwire` in your agent, for example:

> Use golang-doc-ripwire to audit the cache package's documentation and examples. Report unsupported claims and verify that the examples execute.

See [SKILL.md](SKILL.md) for the workflow and [references/ripwire.md](references/ripwire.md) for commands and limitations. The other references and templates retain the upstream guidance, with changes to keep them consistent with the evidence-based workflow.

## Validation

```sh
python3 scripts/check_fixtures.py
python3 scripts/check_fixtures.py --ripwire
```

The first command needs Go and Python 3. It checks the evaluation manifest and compiles/runs a temporary copy of the Go fixture, verifying which examples actually execute. The second also checks seeded Markdown drift and comment-coherence behavior using the installed Ripwire. It fails clearly if Ripwire is unavailable; ordinary skill use still supports a fallback.

These are fixture smoke checks, not an automated claim that all agent evaluations passed. [evals/README.md](evals/README.md) describes the behavioral evaluations and intentional defects in the fixture. Never copy its documentation into a real project.

## Provenance and license

Derived from Samuel Berthe's [`golang-documentation`](https://github.com/samber/cc-skills-golang/tree/19a0626ae8565d27a7b7bdf59d8d99d94d7e284c/skills/golang-documentation), version 1.3.2, from [`samber/cc-skills-golang`](https://github.com/samber/cc-skills-golang) at commit `19a0626ae8565d27a7b7bdf59d8d99d94d7e284c`. The initial commit in this repository preserves that skill and its templates, references, and evaluations before the Ripwire changes.

The original MIT license and copyright notice are retained in [LICENSE](LICENSE). This repository is a maintained derivative, not the full upstream Go skills collection.
