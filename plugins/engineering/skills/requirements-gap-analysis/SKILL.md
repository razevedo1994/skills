---
name: requirements-gap-analysis
description: >
  Compares project notes (CLAUDE.md by default, or a file the user specifies)
  against the codebase and inserts a TODO [GAP] comment in the most relevant
  source file wherever a documented requirement is missing or only partially
  implemented. Use when the user wants to find gaps between requirements and
  code (e.g. "check what's missing", "what have I not built yet") or wants
  those gaps annotated in source as TODOs.
version: 1.0.0
---

# Requirements Gap Analysis

## Overview

This skill compares your project notes (typically `CLAUDE.md`) to the actual codebase and annotates every gap with a `TODO [GAP]` comment placed directly in the most relevant source file.

Use it when you want to know what you planned but haven't built yet, without leaving your editor.

## Workflow

Follow these steps in order every time this skill is invoked.

### Step 1 — Locate the notes file

- Default: look for `CLAUDE.md` in the project root.
- If the user specified a different file, use that.
- Read the full file and extract every requirement, planned feature, or goal. See `references/gap-patterns.md` for extraction heuristics.

### Step 2 — Build a requirements list

From the notes file, produce a flat list of discrete requirements. Each item should be one thing to build or behavior to support. Label each with a short ID (R1, R2, …) for tracking.

Example output of this step (internal, not shown to user):
```
R1: User can log in with email and password
R2: Passwords are hashed with bcrypt
R3: Session expires after 30 minutes of inactivity
R4: Admin panel shows all registered users
```

### Step 3 — Search the codebase for each requirement

For each requirement, grep the codebase for relevant keywords and function names. Consult `references/gap-patterns.md` for keyword mapping strategies.

Classify the result as one of:
- `implemented` — clear, working code covers this requirement
- `partial` — related code exists but the requirement is not fully satisfied
- `missing` — no relevant code found

### Step 4 — Annotate gaps

For each `partial` or `missing` requirement:

1. Identify the best file to annotate:
   - `missing`: the file most related to the domain (e.g., `auth.py` for an auth requirement). If nothing is related, use the project's main entry point.
   - `partial`: the function or class where the gap exists.

2. Insert a TODO comment immediately above the relevant line (or at the top of the file for `missing`):

   **Python / Shell / Ruby:**
   ```python
   # TODO [GAP]: <requirement text> (source: CLAUDE.md)
   ```

   **JavaScript / TypeScript / Go / Java / C:**
   ```js
   // TODO [GAP]: <requirement text> (source: CLAUDE.md)
   ```

   **HTML / XML:**
   ```html
   <!-- TODO [GAP]: <requirement text> (source: CLAUDE.md) -->
   ```

Do not add a TODO for `implemented` requirements.

### Step 5 — Print summary

After annotating, print a summary table:

```
Requirements Gap Analysis — CLAUDE.md
──────────────────────────────────────────────────────────────────
 ID   Status        File annotated               Requirement
──────────────────────────────────────────────────────────────────
 R1   ✅ implemented  —                            User login
 R2   ⚠️  partial     src/auth.py:32               Password hashing
 R3   ❌ missing      src/auth.py (top)            Session timeout
 R4   ❌ missing      src/admin.py (top)           Admin user list
──────────────────────────────────────────────────────────────────
2 implemented · 1 partial · 2 missing (3 TODOs added)
```

## Reference

For detailed extraction heuristics, keyword mapping strategies, and edge cases see:
`references/gap-patterns.md`
