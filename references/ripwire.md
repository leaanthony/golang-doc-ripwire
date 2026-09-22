# Ripwire recipes for Go documentation

Use the smallest recipe that answers the task. Commands below assume a shell at the repository root and placeholders replaced with real package paths or symbols. These are read-only inspection commands; running examples executes the repository's Go code.

## Availability and scope

Run `ripwire --version` and consult `ripwire --help` for uncertain flags. This integration was probed with Ripwire 0.5.0, build `bacfa3b7b`; future builds may improve support. Missing binaries, unsupported commands, and incomplete results are reasons to fall back, not to abandon documentation work.

For a complete audit, use `go list ./...` within each relevant module and inspect declarations with `go doc -all <package>` and source. A module workspace may need one invocation per member module. Honor the project's build tags and target platforms. Generated sources, ignored paths, other modules, and build-tag variants need an explicit inclusion decision. A ranked Ripwire map is a reading order, never the exported-API denominator.

Check `capped`, `shown`, `unchecked`, ambiguity, and missing/ignored-file disclosures before treating absence as evidence. Page supported commands with `--limit`/`--offset`, narrow the scope, or read source. Use `--skipped` when a known file is missing, and `--doctor` if an indexing problem remains. Do not repeatedly diagnose an unavailable tool when ordinary Go tooling can answer the question.

## Ground a comment or package explanation

```bash
ripwire . --recall="cache expiration and ownership"
ripwire . --for="Lookup"
ripwire . --expand=cache.go:Lookup
# Only if usage or a callee's behavior is still unclear:
ripwire . --callers=cache.go:Lookup
ripwire . --callees=cache.go:Lookup
```

A conceptual query can return signatures without bodies; select the relevant symbol before expanding. Read comments immediately above its declaration if expansion omits them. Do not run each command mechanically when the supplied source already establishes the requested fact.

Keep these distinctions in the working evidence:

| Claim | Evidence needed |
| --- | --- |
| Current behavior | Implementation, relevant callees, and tests exercising the behavior |
| Intended interface obligation | Interface comment, authoritative design decision, or explicit user requirement |
| Actual caller usage | Caller body or example; usage alone does not define every valid input |
| Why the design exists | Recorded decision or user context; structure alone cannot establish intent |
| Concurrency, cancellation, ownership | Relevant synchronization/control flow and contract; no guarantee from names or signatures alone |
| Performance | Appropriate measured evidence for performance claims; complexity/fan-in is not runtime measurement |

A mismatch between a contract and implementation is a finding. Report both and determine which is wrong before rewriting the contract. Unresolved claims should stay visible in the review, not become invented guarantees.

## Review comments and Markdown

```bash
ripwire . --comment-coherence --limit=40
ripwire . --doc-drift=README.md
ripwire . --mentions=Lookup
```

**Comment coherence:** high `c_coeff` means more words resemble the symbol name. `cic` measures vocabulary overlap with implementation identifiers, a different axis. These lexical signals can prioritize manual review but do not prove accuracy or usefulness. Preserve short comments that fully explain a simple API. `no_comment` includes eligible functions without comments, potentially tests and examples; it is not a missing-exported-docs count and excludes other API kinds such as fields and types.

**Doc drift:** checks selected anchors in Markdown, including file/line references, symbol mentions, integer constants, and array extents where supported. It does not validate prose, fenced snippets, source doc comments, web links, or `llms.txt`. An absent finding means no supported contradiction was found. Inspect `checked`, `unchecked`, and any cap/unread-file disclosures. Mention detection deliberately under-reports and can decline uncorroborated names. Exit 0 means the report ran, not that documentation is correct; CI must inspect findings under an explicit policy if a gate is desired.

`--doc-drift --with-history` can distinguish historically removed names from names never established in the available history. Shallow or incomplete history limits that conclusion. Date annotations can classify failed anchors as historical records: do not add dates to live docs merely to suppress drift. `--gateability` is not a semantic verification gate.

**Mentions:** locates Markdown references in supported forms such as backticked symbol names. Use `rg` as well when updating prose, Go `[Symbol]` links, qualified names, examples, or other file formats. For a literal search through Ripwire, `--grep-in=any` avoids suppressing comment and string hits:

```bash
ripwire . --grep=Lookup --grep-in=any --grep-context=2
```

## Write and verify examples

Inspect existing callers/examples before adding another scenario. `--exercises=<test-file>` shows structural reach from an indexed test file; `--affected=SYM` identifies candidate test files to run. Neither proves Go discovered or executed an example, and a missing graph edge does not prove a missing test.

```bash
ripwire . --callers=Lookup
ripwire . --exercises=cache_test.go
ripwire . --affected=Lookup
go test -v -run '^Example' -count=1 ./cache
```

Use the actual package path in place of `./cache`. Confirm the expected example names have run/pass events. `Output:` supports exact output, `Unordered output:` is appropriate only when order is not part of the contract, and an empty `Output:` still requests execution. No output directive means compile-only. A green command saying no tests ran does not verify behavior. Keep examples deterministic and self-contained where practical; do not alter production behavior to fit an example.

Go's test runner is authoritative for example discovery and execution. Ripwire test reachability is neither line coverage nor an assertion-quality measure. A package may compile while all of its examples remain unexecuted.

## Go interface and graph limitations

In the tested build, `--lego=Store` on a real Go interface returned `methods="0" caveat="not-extracted-for-lang"` and `implementors="0"` despite a valid implementation. Do not use that surface to enumerate Go method contracts or declare there are no implementations. Read declarations and use Go's type checker/tests to confirm implementation claims, including pointer/value method-set differences and embedded interfaces.

Call edges can be ambiguous or missing for interface dispatch, callbacks, reflection, and external consumers. Confirm edges before stating a flow as fact. Zero callers does not mean a public library API is unused. Use `--path=A,B` for directed call paths and `--connect=A,B,C` for relationships; neither proves runtime ordering, conditional execution, or asynchronous delivery.

For architecture documentation, retrieve recorded rationale separately from the structural map. Do not label graph communities as Go packages without checking their membership.

## Large audits and changes

One `--pack-task="<task>" --partition=N` can provide shared context and agent slices. Inspect overlap and any split communities before assigning disjoint file ownership. A coordinator keeps the exhaustive Go package inventory and reconciles shared docs. A graph partition cannot replace that inventory.

For documentation updates driven by a diff, inspect the actual diff first, then run `--mentions` on the changed symbols and a scoped drift review. Use `--pr-context` only when broader code review is part of the task; do not add a merge audit to a wording change.

If executable code changes, companion skills may call for `--quality-delta`, `--edit-check=SYM`, and `--affected`. Read their actual findings and run Go tests. A clean structural delta does not prove correctness, prose quality, or semantic contract preservation; the fast contract check does not verify every aspect of Go type compatibility. `--test-gate` reports obligations and cannot observe that a test command passed.

Record the revision (`git rev-parse HEAD`) and working-tree state (`git status --short`) for a substantial review. `+dirty` results describe local changes that cannot be recovered from the commit alone. Report tool unavailability and exclusions without claiming complete coverage.

## Fallback without Ripwire

Use `go list` plus source declarations for inventory, `go doc` for documentation inspection, `rg` and targeted reads for references/call sites, and `go test` for runnable examples. Review Markdown claims and links manually against source. A small supplied code snippet may already contain all necessary evidence. Missing Ripwire never permits unsupported guarantees or a claim that a skipped check passed.
