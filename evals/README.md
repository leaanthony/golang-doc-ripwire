# Evaluating the skill

`evals.json` contains 21 inherited writing/review scenarios and eight new fixture-backed scenarios. Inherited expectations were revised where they rewarded ignoring user scope, forcing verbose comments, inventing Playground links, or treating templates as verified facts.

## Behavioral evaluation procedure

For each case, use a fresh agent context with this skill and the case's `prompt`. For a case with `fixture`, copy that directory to an isolated writable workspace and provide its location. Do not provide the evaluator's assertions, trap description, or the answer key below to the agent performing the task. Compare its output, commands, and diff with the assertions. Record pass/fail per assertion, tool versions, and the skill revision. A manifest or fixture check is not a behavioral evaluation pass.

For `ripwire-unavailable`, use a sandbox without Ripwire on PATH (or with execution of that binary disabled), while retaining Go and ordinary read/search tools. Do not change the user's installed toolchain. For `incomplete-ripwire-results`, provide a capped initial report or impose a small query budget; retain direct source access. Keep external publication disabled in all cases unless a case explicitly requires it.

## Fixture answer key

`fixtures/doc-audit` is a compilable Go module containing a library and a CLI. Its docs intentionally contain errors:

- `MaxEntries` is 8, not 99, and is not an enforced cache capacity.
- `missing.go:12` does not exist.
- Cache operations do not synchronize concurrent map access; the README's concurrent read/write claim is false.
- The command's `-key` default is `name`, not `user`.
- `Reset` is exported and undocumented, with no production callers.
- `ExampleLookup` has output and runs. `ExampleCache_Get` compiles but does not execute.
- The fenced `RemovedLookup` example is invalid and is outside doc-drift's snippet-validation scope.
- `*Cache` satisfies `Reader`, checked by a Go compile-time assertion. Ripwire support must not be inferred from a zero result.
- `Set sets.` is name-restating; Get's existing return-value comment is useful despite its brevity.

Do not repair these intentional defects in the committed fixture. Agent edits belong only in disposable copies.

## Smoke checks

From the repository root, run `python3 scripts/check_fixtures.py`, optionally adding `--ripwire` to exercise the installed Ripwire on the fixture. The checks validate manifest IDs and fixture paths, Go package discovery, example execution, planted drift detection, and comment ranking. The script uses a temporary copy and never rewrites the committed fixture. It does not assert that Go interface extraction must remain unsupported in future Ripwire versions.

## Initial forward test

On 2026-09-22 an independent agent received the skill and an isolated fixture copy, without this answer key or the evaluation assertions. Its task was to review documentation and examples, verify example execution, and recommend a package documentation strategy. Using Go 1.26.5 on darwin/arm64 and Ripwire 0.5.0 (`bacfa3b7b`), it identified the seeded constant, source-reference, concurrency, CLI-default, example-execution, and fenced-snippet errors, plus missing Reset documentation. It distinguished the library and command audiences and left the copy unchanged. This was one combined behavioral scenario, not a complete run of all 29 cases.

The Ripwire quality delta against the upstream import flags the larger evaluation JSON array as verbosity and the deliberately similar example functions as duplication. These are intentional evaluation data: the added cases exercise new behavior, and the paired examples test the compile-only distinction. They are retained without suppressing the findings; neither is a prose-correctness verdict.
