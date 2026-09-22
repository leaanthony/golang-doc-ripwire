# Project Documentation

Optional companion, if installed: `samber/cc-skills-golang@golang-continuous-integration` skill for automating changelog generation and release workflows.

## Table of Contents

- [README.md](#readmemd)
  - [Section Order](#section-order)
- [CONTRIBUTING.md](#contributingmd)
  - [The 10-Minute Rule](#the-10-minute-rule)
- [Changelog](#changelog)
  - [Format](#format)
  - [Change Categories](#change-categories)
  - [GitHub Releases as Alternative](#github-releases-as-alternative)
- [Distribution](#distribution)
  - [Dockerfile Best Practices](#dockerfile-best-practices)

## README.md

Link the existing license; flag its absence without selecting license terms for the user. The README is the project's front page — make it simple, clear, and scannable. A copy-paste template with empty sections is available at [templates/README.md](../assets/templates/README.md).

### Section Order

For a new README, this is a suggested order. Preserve the project's existing structure and the user's preferences; omit empty sections and unverified badges:

1. **Title** — project name as `# heading`
2. **Badges** — shields.io pictograms (Go version, license, CI, coverage, Go Report Card)
3. **Summary** — 1-2 sentences explaining what the project does
4. **Demo** — code snippet (libraries), GIF/video (CLIs), or screenshot (web UIs)
5. **Getting Started** — installation + minimal working example
6. **Features / Specification** — verified capabilities, organized by feature area without padding
7. **Contributing** — link to CONTRIBUTING.md or inline if very short
8. **License** — license name + link

The template includes commented-out sections for applications (binary download table, Docker, Homebrew) that you can uncomment as needed.

---

## CONTRIBUTING.md

The goal: a new contributor should be able to clone the repo, make a change, and run the tests **in under 10 minutes**. If setup takes longer, identify the friction and suggest tooling improvements; implement infrastructure only when it is within the requested scope.

Copy the template from [templates/CONTRIBUTING.md](../assets/templates/CONTRIBUTING.md).

### The 10-Minute Rule

If setup takes more than 10 minutes, consider these improvements. Document only commands that actually exist; proposed tools must be labeled as proposals:

| Problem | Solution |
| --- | --- |
| Complex build steps | Add a `Makefile` with `make build`, `make test`, `make lint` |
| External service dependencies | Add `docker-compose.yml` for local dev |
| Inconsistent dev environments | Add `.devcontainer/` for VS Code devcontainers |
| Slow test suite | Separate unit tests (fast) from integration tests (build tags) |
| Missing documentation | Add `make help` that lists available targets |

---

## Changelog

CHANGELOG MUST be updated for every release, tracking the notable changes it contains. Use [Keep a Changelog](https://keepachangelog.com/) format. Copy the template from [templates/CHANGELOG.md](../assets/templates/CHANGELOG.md).

### Format

```markdown
## [1.2.0] - 2026-03-08

### Added

- New `WithTimeout` option for client configuration

### Changed

- Improved retry logic to use exponential backoff

### Fixed

- Race condition in connection pool under heavy load

### Deprecated

- `SetTimeout()` method — use `WithTimeout()` option instead

[1.2.0]: https://github.com/{owner}/{repo}/compare/v1.1.0...v1.2.0
```

### Change Categories

- **Added** — new features
- **Changed** — changes in existing functionality
- **Deprecated** — features that will be removed
- **Removed** — removed features
- **Fixed** — bug fixes
- **Security** — vulnerability fixes

### GitHub Releases as Alternative

For simpler projects, GitHub Releases can replace a CHANGELOG file. GoReleaser auto-generates release notes from git commits.

---

## Distribution

Document installation paths the project actually supports. Additional binaries, containers, or package-manager distribution may be useful proposals, but do not claim they exist or implement them solely to fill a documentation template.

### Dockerfile Best Practices

For a project already using containers, document its actual build. This multi-stage example is illustrative; use the Go version and image pinned by the project rather than copying an unverified tag:

```dockerfile
# Build stage
ARG GO_IMAGE
FROM ${GO_IMAGE} AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/binary ./cmd/server

# Final stage
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/binary /binary
ENTRYPOINT ["/binary"]
```
