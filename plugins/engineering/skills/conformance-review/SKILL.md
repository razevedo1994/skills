---
name: conformance-review
description: Review the changes since a commit, branch, tag, or merge-base along three independent axes — conformance to this repo's documented coding standards (CLAUDE.md, CONTRIBUTING.md, style/lint configs), conformance to the system behavior documented in CONTEXT.md/CLAUDE.md/ADRs, and code smells with concrete resolutions. Use when the user wants to review a branch, a PR, or work-in-progress changes for standards or spec conformance, or asks for a code smell pass.
---

# Conformance Review

Reviews the diff since a fixed point along three independent axes — **standards** (does the code follow this repo's documented conventions?), **spec** (does the code match the system behavior documented in `CONTEXT.md`/`CLAUDE.md`/ADRs?), and **smells** (does the code exhibit recognized code smells, and how should each be resolved?) — run as parallel sub-agents and reported side by side.

This is not a bug hunt. Correctness findings belong to `/code-review`; this skill only checks conformance to what's written down, plus quality smells within the diff itself.

## 1. Fix the diff range

If the user named a fixed point (commit SHA, branch, tag), diff against that. Otherwise compute the merge-base between `HEAD` and the repo's default branch and diff against that.

Completion criterion: you have a single diff range and the list of files it touches.

## 2. Gather the standards documents

Collect whichever of these exist: root `CLAUDE.md`, any `CLAUDE.md` in a changed file's directory or an ancestor of it, `CONTRIBUTING.md`, `STYLEGUIDE.md`/`STYLE_GUIDE.md`, `.editorconfig`, and linter/formatter configs relevant to the changed file types (`.eslintrc*`, `.prettierrc*`, `pyproject.toml` `[tool.ruff]`, `rustfmt.toml`, etc.).

Completion criterion: every changed file's directory chain has been checked for a governing `CLAUDE.md`, and the applicable convention files are listed (even if the list is empty).

## 3. Gather the spec documents

Collect whichever of these exist: root `CLAUDE.md`, `CONTEXT.md`/`CONTEXT-MAP.md` (and the `CONTEXT.md` of any bounded context the diff touches), and `docs/adr/*.md` (root and per-context).

If the diff touches behavior that none of these documents constrain — the domain model is silent on it — do not guess at what "correct" means. Stop and ask the user whether they want a `/grill-with-docs` (or `/domain-modeling`) session first to pin down the missing constraints, or want the spec axis marked "undocumented" for that area and the review to proceed anyway.

Completion criterion: for every changed behavior, you can state which doc (if any) constrains it.

## 4. Run all three reviews in parallel

Spawn three agents in parallel, in a single message:

- **Standards agent** — reviews the diff strictly against the documents from step 2 (naming, structure, error handling, formatting, lint rules). Returns findings as `file:line` + one-line summary, or an explicit "no issues found."
- **Spec agent** — reviews the diff strictly against the documents from step 3: does the code do what `CONTEXT.md`/ADRs say the system does, does it use the canonical domain terms, does it violate a stated ADR decision. Returns findings the same way.
- **Smells agent** — reviews the diff for recognized code smells (see below), scoped to lines the diff actually touches or that the diff makes worse — not a pre-existing smell the diff leaves untouched. For each smell found, names the smell, points at `file:line`, and states a concrete resolution (the refactoring to apply, not just "clean this up").

Give each agent the diff range and only its own material — don't let the standards/spec documents leak into the smells agent's review, and vice versa. Instruct all three explicitly: read-only, do not edit files, report findings only.

Completion criterion: all three agents have returned, each with either a finding list or an explicit "no issues found."

### Code smells to check for

- **Duplicated logic** — the same block of logic repeated instead of extracted. Resolution: extract a function/method, or unify the call sites.
- **Long method / long function** — a function doing too many distinct things to name in one sentence. Resolution: extract the sub-steps into named functions.
- **Large class / god object** — a class or module accumulating unrelated responsibilities. Resolution: split along the seams of its responsibilities.
- **Long parameter list** — a function that takes more parameters than callers can track. Resolution: group related parameters into a single object/struct.
- **Feature envy** — a function that uses another object's data more than its own. Resolution: move the function (or the piece that envies) to the object it's really operating on.
- **Primitive obsession** — a bare string/number/bool standing in for a domain concept that deserves its own type. Resolution: introduce a small type or value object for it.
- **Shotgun surgery** — a single conceptual change requires editing many unrelated files. Resolution: consolidate the scattered logic behind one seam.
- **Deep nesting / arrow code** — conditionals or loops nested past what's readable. Resolution: invert conditions to guard clauses, or extract the nested block into its own function.
- **Dead code** — code the diff adds or leaves behind that nothing reaches. Resolution: delete it.
- **Speculative generality** — abstraction (interface, config flag, hook) built for a use case that doesn't exist yet. Resolution: inline it back until a second real caller justifies the abstraction.
- **Inconsistent naming** — the same concept named differently across the diff, or a name that no longer matches what the code does. Resolution: pick one name and apply it everywhere.

## 5. Report side by side

Render the three result sets as a single markdown table, columns `Standards` | `Spec` | `Smells`, one row per finding (pad shorter columns with blank cells). Standards/Spec cells: `file:line` — one-line summary. Smells cells: `file:line` — smell name — resolution. If the spec axis was skipped entirely (step 3, undocumented behavior), say so in that column instead of leaving it silently empty.
