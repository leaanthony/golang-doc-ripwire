---
name: golang-doc-ripwire
description: Write and review Go documentation grounded in source code, actual usage, and executable examples. Use for Go doc comments, package docs, README, CONTRIBUTING, changelogs, configuration and API docs, or documentation drift audits. Uses Ripwire when available, with Go tooling and focused source reads as a fallback.
license: MIT
metadata:
  author: leaanthony
  version: "0.1.0"
  upstream: samber/cc-skills-golang@golang-documentation
  upstream-version: "1.3.2"
  homepage: https://github.com/leaanthony/golang-doc-ripwire
allowed-tools: Read Edit Write Glob Grep Bash(go:*) Bash(gofmt:*) Bash(golangci-lint:*) Bash(git:*) Bash(ripwire:*) Bash(rg:*) Agent WebFetch
---

# Go Documentation with Ripwire

Write documentation for readers who have not seen the code. Establish the relevant facts before describing them, and verify examples with Go tooling.

## Scope and modes

Follow the user's requested scope and repository conventions. A request for one comment does not require a repository-wide audit, README rewrite, new infrastructure, or publication to an external service.

- **Write:** create or improve the requested documentation, preserving behavior and existing obligations.
- **Review:** report accuracy, completeness, and clarity findings with source locations; edit only when requested.
- **Update after code changes:** identify documentation affected by the actual change and verify those claims again.

For large tasks, see [Parallel work](#parallel-work). Otherwise work locally and stop gathering evidence once the question is answered.

## Writing principles

- Explain behavior, purpose, constraints, and relevant failure modes. Avoid merely restating signatures, but do state what a function does or returns.
- Keep the shortest wording that carries the necessary facts. A useful one-line comment is sufficient for a simple API; honor requests for brevity.
- Support concurrency, cancellation, ownership, nil/zero-value behavior, errors, ordering, resource lifetime, and performance claims with relevant evidence. An interface contract can state an intended obligation; one implementation or caller does not prove all implementations satisfy it.
- Preserve `must`, `should`, and `may`, conditions, and warnings. When docs and code conflict, report the discrepancy rather than silently treating a possible bug as the new contract.
- Do not invent design rationale, error guarantees, roadmap commitments, installation methods, or working Playground links. Treat templates as illustrative; replace placeholders only with verified project facts.

## Step 0: Establish documentation evidence

1. **Scope the surface.** Identify the relevant module/package, audience, and requested artifact. For a complete audit, inventory packages with `go list ./...` from each relevant module and inspect exported declarations through `go doc -all` and source. Include types, methods, fields, constants, variables, and package comments. Record build tags, platform scope, generated files, or package-load failures that limit the inventory. Ripwire rankings and local caller counts are not an exhaustive public API census.
2. **Retrieve existing context.** Use `ripwire <repo> --recall="<topic>"` for existing documentation and decisions. For unfamiliar code, use `--for="<topic>"` or one bounded `--pack-task="<task>"`. Retrieved docs are claims to check, not proof of current behavior.
3. **Inspect relevant code and usage.** Use `--expand=SYM` and, when useful, `--callers=SYM`, `--callees=SYM`, or `--uses=SYM`. Read the preceding source comment if the body excludes it. Confirm ambiguous edges and consequential behavior in source and tests. Prefer file-qualified symbols when names collide.
4. **Keep claim evidence.** For substantial reviews, record each important claim, its source/test or design decision, and whether it is observed, intended, contradicted, or unresolved. Put citations in the review; avoid adding an evidence ledger to every public doc comment.

Read [Ripwire recipes and limitations](references/ripwire.md) when using the commands above or auditing drift. Check the installed `ripwire --version`/`--help` when capability support is uncertain. If Ripwire is missing, fails, or has insufficient language support, continue with `rg`, focused source reads, `go list`, `go doc`, and tests. Do not install tools or alter agent configuration just to perform a documentation task.

## Step 1: Determine the documentation audience

Classify packages and deliverables, not the entire repository from the presence of `main` or `cmd/` alone. A repository can contain both importable libraries and command packages.

- **Library:** prioritize package/API comments and runnable examples. Read [Library documentation](references/library.md).
- **Application/CLI:** prioritize verified installation methods, help text, flags, configuration, and operations. Read [Application documentation](references/application.md).
- **Mixed repository:** document the library contract and command usage separately, linking shared concepts.
- **Private project:** keep examples and documentation local or within its existing internal systems. Public indexing and Playground publication are not part of a routine documentation edit.

## Step 2: Select the relevant deliverables

Use this as an audit checklist within the agreed scope, not a mandate to create every file:

| Surface | What to verify |
| --- | --- |
| Exported API and package comments | Purpose, behavior, constraints, errors, useful zero values, and field meanings |
| README / getting started | Project purpose, supported installation, minimal working usage, and valid links |
| Working examples | Public API usage, deterministic output, real execution |
| CONTRIBUTING | Actual prerequisites, build/test commands, contributor workflow |
| CHANGELOG or releases | Notable user-visible changes supported by the release diff/history |
| CLI/configuration docs | Actual flags, defaults, required values, and precedence |
| Protocol/API docs | Agreement with handlers, schemas, protobuf, and configured generators |
| Architecture docs | Verified entry points and flows; separately sourced design rationale |
| llms.txt / documentation site | Useful navigation when requested or already part of the project |
| License | Link to the existing license; flag its absence without choosing legal terms |

## Parallel work

When a large documentation task warrants delegation and agents are available, establish the package inventory and shared evidence once. `ripwire <repo> --pack-task="<task>" --partition=N` can supply shared context plus slices; inspect `overlap_max`, `split`, and the actual partition count before using them. Graph communities are not necessarily Go packages.

Assign disjoint files/packages and explicit output ownership. One editor owns shared README/package summaries and reconciles terminology and contracts. Each worker returns changes or findings, supporting locations, checks run, and unresolved claims. Reduce the number of workers when the surface is tightly coupled; without delegation, use the same scopes sequentially.

## Step 3: Write or review doc comments

Document exported functions, methods, types, interfaces, constants, variables, and meaningful exported fields. Add internal comments where reasoning or constraints are non-obvious. Ordinary test functions do not need boilerplate comments; explain unusual setup when useful or explicitly requested.

Start function/method comments with a complete sentence naming the symbol. Include only the details callers need to use it correctly; do not require Parameters, Returns, and Example sections on every function. The name-prefix convention supports clarity and search, not a rendering prerequisite.

Before asserting stronger guarantees, check the evidence from Step 0. For example, context acceptance alone does not prove cancellation, and a map-backed type is not automatically safe for concurrent mutation. For interfaces, inspect the declaration and relevant implementations using Go tooling; do not rely on Ripwire's `--lego` to establish Go method sets or implementation completeness.

In review mode, `--comment-coherence` can prioritize comments that repeat names. It is a lexical heuristic, not a prose grade or missing-docs census. Never pad a concise correct comment to improve a score. Read [Code comments](references/code-comments.md) for formatting and examples, and [Ripwire review recipes](references/ripwire.md#review-comments-and-markdown) for interpreting findings.

## Step 4: Project documentation

Use the existing structure unless the user requests a redesign. For a new README, [the template](assets/templates/README.md) offers title, badges, summary, demo, getting started, features, contributing, contributors, and license sections. Omit empty sections and unsupported badges; a feature list should be as long as the actual product requires.

CONTRIBUTING should document the real setup and test workflow. If setup is cumbersome, identify the problem and suggest improvements rather than silently adding infrastructure. For changelogs, describe user-visible changes supported by history; use the project's release format or [the changelog template](assets/templates/CHANGELOG.md).

Read [Project documentation](references/project-docs.md) for details. For architecture, combine a targeted `--report`, `--path`, or `--connect` with source reads; source design intent from decisions retrieved by `--recall`. Label inferred edges and unresolved behavior. Graph metrics alone cannot establish runtime order, performance, or delivery status.

## Step 5: Examples, applications, and APIs

- **Library examples:** inspect real callers and existing examples before adding `ExampleXxx` functions. Prefer a small set of useful public-API scenarios over repetitive examples for every symbol. Use deterministic `// Output:` or `// Unordered output:` when runtime verification is intended. Without one, an example compiles but does not execute. See [Library documentation](references/library.md).
- **CLI/configuration:** trace flag/env/config declarations and loading order. Verify defaults and precedence against implementation, tests, or safe help invocations; do not copy the illustrative precedence in a template as fact. See [Application documentation](references/application.md).
- **APIs:** use the existing schema/protobuf/annotation workflow. Inspect generator configuration before claiming a specification version or adding a tool. Document supported behavior and error responses.
- **AI navigation:** when requested, use [llms.txt](assets/templates/llms.txt) to link maintained docs. Verify its paths and claims; Ripwire's Markdown drift pass does not establish that a `.txt` file or its links are valid.

## Step 6: Verify and deliver

1. Review the diff and links, then preview affected package/symbol documentation with `go doc`. Formatting and semantic claims still need inspection; `go doc` alone is not a completeness gate.
2. When Go files change, format the changed files with `gofmt`. Run new/changed examples in the affected packages with `go test -v -run '^Example' -count=1 <packages>` and confirm their names actually execute. A successful exit with no examples run is not runtime verification. Compile-only examples are acceptable when intentional and reported as such.
3. For Markdown changes or a code-driven docs update, run a scoped `--doc-drift` and inspect the findings and unchecked counts. Use `--mentions=SYM` for changed symbols plus a text search for other references. Neither command checks arbitrary prose or fenced code. Recheck snippets against source and execute runnable examples separately.
4. When executable code changes, run appropriate Go tests and repository-required checks. Ripwire's `--affected` helps select tests but does not run or prove discovery of them. Use code quality/contract checks when relevant; they are not documentation quality scores. Avoid expanding a prose-only change into a code refactor.
5. Report the documentation changed or findings found, checks actually performed, and unresolved claims or scope limits. Tie substantial audit evidence to the measured revision and dirty state. Never report “all docs verified” solely from a clean graph or drift result.

## Sources and optional companion skills

- [Go doc comments](https://go.dev/doc/comment) and [Go examples](https://pkg.go.dev/testing#hdr-Examples) are authoritative for Go conventions.
- If installed, Ripwire orient/navigate/fresh-eyes skills provide additional retrieval and review guidance; write-tests/change-check apply when executable examples or code change. This skill remains usable without them.
- Derived from `samber/cc-skills-golang`'s `golang-documentation` 1.3.2; see [README](README.md) for provenance and [LICENSE](LICENSE).
