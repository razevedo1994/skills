# Gap Detection Patterns

Reference for Step 2 (requirement extraction) and Step 3 (gap classification) of the requirements-gap-analysis skill.

---

## Extracting Requirements from Markdown

Parse the notes file top-to-bottom. Treat each of the following as a discrete requirement:

| Pattern | Example | Extract as |
|---------|---------|------------|
| Checkbox (unchecked) | `- [ ] Add login page` | Requirement (probably missing) |
| Checkbox (checked) | `- [x] Add login page` | Skip — likely done |
| Bullet under "Features", "Goals", "TODO", "Planned", "Roadmap" heading | `- User can reset password` | Requirement |
| Numbered list item under similar headings | `1. Rate-limit the API` | Requirement |
| Inline bold/heading like `**Auth**` followed by bullets | Sub-bullets | Flatten into individual requirements |
| Plain sentences in "Goals" or "Overview" sections | `The app should support OAuth.` | Requirement |

**Skip:** changelog entries, completed work sections (`## Done`, `## Completed`), commentary, and examples.

---

## Keyword Mapping for Codebase Search

When classifying a requirement, search for these keyword clusters. A hit in at least two different keywords = likely `implemented`. A hit in only one = `partial`. Zero hits = `missing`.

| Domain | Keywords to grep |
|--------|-----------------|
| Authentication | `login`, `auth`, `session`, `token`, `jwt`, `oauth`, `password`, `credential` |
| User management | `user`, `register`, `signup`, `profile`, `account`, `role`, `permission` |
| Database / persistence | `db`, `database`, `model`, `migration`, `repository`, `store`, `save`, `persist` |
| API / HTTP | `route`, `endpoint`, `handler`, `controller`, `request`, `response`, `status` |
| File handling | `upload`, `download`, `file`, `stream`, `storage`, `bucket`, `blob` |
| Notifications | `email`, `notify`, `notification`, `webhook`, `alert`, `send` |
| Scheduling / background | `cron`, `job`, `task`, `queue`, `worker`, `schedule`, `async` |
| Search | `search`, `query`, `filter`, `index`, `fulltext`, `elastic` |
| Payment | `payment`, `stripe`, `charge`, `invoice`, `billing`, `subscription` |
| Admin | `admin`, `dashboard`, `panel`, `backoffice`, `manage` |

For requirements outside these domains, extract the 2-3 most distinctive nouns from the requirement text and grep for those.

---

## Classifying "Partial"

A requirement is `partial` when:

- A function or class exists with the right name, but key logic is absent (e.g., `hash_password` exists but calls `md5` instead of `bcrypt`)
- A route is defined but returns a stub/placeholder (`TODO`, `pass`, `return nil`, `throw new Error("not implemented")`)
- Only the happy path is handled and the requirement mentions edge cases (e.g., "must handle expired tokens" but there's no expiry check)
- A test file references the feature but the implementation is empty or skipped

---

## Where to Place the TODO

### `missing` requirement — no related code found

1. If the requirement clearly belongs to a domain (auth, payments, etc.), find the file most associated with that domain (e.g., `auth.py`, `payments.js`). Insert the TODO at the very top of the file, below any imports.
2. If no domain file exists, insert at the top of the project's main entry point (`main.py`, `app.py`, `index.js`, `main.go`, etc.).
3. If the project has no clear entry point, create a `GAPS.md` file at the project root and list the missing requirements there as checkboxes.

### `partial` requirement — related code found

Insert the TODO on the line immediately above the function, method, or class where the gap exists. If the gap spans multiple locations, annotate only the most central one and mention the others in the comment.

---

## TODO Comment Text

Keep the requirement text verbatim from the notes file — don't paraphrase. This makes it easy to grep for `TODO [GAP]` later and cross-reference with the source doc. See SKILL.md Step 4 for the comment format itself.

Example of a `partial` annotation:
```python
# TODO [GAP]: Passwords are hashed with bcrypt (source: CLAUDE.md)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

---

## Edge Cases

**Requirement is too vague to search for** (e.g., "make it fast"): skip it unless there's a concrete measurable sub-requirement implied. Note it in the summary as `skipped (too vague)`.

**Same requirement mentioned multiple times in notes**: deduplicate; annotate once.

**Notes file has no structured requirements**: fall back to the "Goals" or first-level heading sections and extract sentences that contain action verbs (should, must, will, can, need to).

**Binary/generated files in codebase**: skip them during search.

**Test files only**: a test that tests a feature counts as a hint of `partial`, not `implemented`, unless the corresponding production code is also present.
