# Personal Skills

A personal collection of [Agent Skills](https://code.claude.com/docs/en/skills) — reusable, model-invoked instructions that extend coding assistants with specialized workflows.

This repo is a Claude Code **plugin marketplace** (`.claude-plugin/marketplace.json`): skills are grouped by category, and each category is one installable plugin under `plugins/<category>/`, so you can install just the categories you want instead of pulling in the whole collection.

```
.claude-plugin/
  marketplace.json                 # lists every plugin (category) in this repo
plugins/
  engineering/
    .claude-plugin/plugin.json     # this category's plugin manifest
    skills/
      requirements-gap-analysis/
        SKILL.md                   # find gaps between docs and code
        references/
        evals/
  productivity/
    .claude-plugin/plugin.json     # this category's plugin manifest
    skills/
      writing-great-skills/
        SKILL.md                   # vocabulary/principles for writing skills
        GLOSSARY.md
```

Each skill folder contains a `SKILL.md` with YAML frontmatter (`name`, `description`) plus the instructions, and optional `references/` or `evals/` subfolders with supporting material.

## Available skills

| Category | Skill | Description |
|---|---|---|
| Engineering | [`requirements-gap-analysis`](plugins/engineering/skills/requirements-gap-analysis) | Compares project notes (e.g. `CLAUDE.md`) to the actual codebase and annotates gaps with `TODO` comments in the relevant source files. |
| Engineering | [`domain-modeling`](plugins/engineering/skills/domain-modeling) | Builds and sharpens a project's domain model as you design: challenges terminology, stress-tests scenarios, and records the glossary (`CONTEXT.md`) and ADRs as decisions crystallise. |
| Engineering | [`grill-with-docs`](plugins/engineering/skills/grill-with-docs) | Runs a `grilling` interview while using `domain-modeling` to capture docs as you go. User-invoked only; requires both the `engineering` and `productivity` plugins. |
| Engineering | [`conformance-review`](plugins/engineering/skills/conformance-review) | Reviews a diff against documented standards (`CLAUDE.md`/`CONTRIBUTING.md`), documented spec (`CONTEXT.md`/ADRs), and code smells — three parallel sub-agent passes reported side by side. |
| Productivity | [`writing-great-skills`](plugins/productivity/skills/writing-great-skills) | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. User-invoked only. |
| Productivity | [`grilling`](plugins/productivity/skills/grilling) | Interviews the user relentlessly, one question at a time with a recommended answer, to stress-test a plan or design before building. |

## Using with Claude Code

**Install a category plugin from the marketplace (recommended)**

1. Add this repo as a marketplace:
   ```
   /plugin marketplace add /path/to/skills
   ```
   Or, once published, `/plugin marketplace add <owner>/<repo>` or a Git/HTTPS URL.
2. Install the category (or categories) you want — installing one pulls in every skill under it:
   ```
   /plugin install engineering@personal-skills
   /plugin install productivity@personal-skills
   ```
3. Restart or reload Claude Code. Run `/plugin marketplace update personal-skills` later to pick up new/updated skills.

Browse everything on offer with `/plugin` or `/plugin marketplace list`.

**As a loose skill (no plugin install)**

Copy or symlink an individual skill folder into one of Claude Code's skill directories:

- Personal, all projects: `~/.claude/skills/<skill-name>/`
- Project-local: `<project>/.claude/skills/<skill-name>/`

```bash
ln -s /path/to/skills/plugins/engineering/skills/requirements-gap-analysis \
      ~/.claude/skills/requirements-gap-analysis
```

**Invoking a skill**

Skills are invoked automatically when your prompt matches their `description`, or explicitly with `/skill-name` (e.g. `/requirements-gap-analysis`).

## Using with Zed

Zed supports Agent Skills the same way Claude Code does. Symlink or copy a skill folder into Zed's skills directory (`~/.config/zed/skills/` or the project's `.zed/skills/`), matching the `<skill-name>/SKILL.md` layout above. See Zed's agent documentation for the exact directory in your installed version, since this has moved across releases.

## Using with opencode

opencode reads skills from `~/.config/opencode/skill/<skill-name>/SKILL.md` (global) or `.opencode/skill/<skill-name>/SKILL.md` (per-project). Copy or symlink a skill folder in, preserving its `SKILL.md` and any `references/`/`evals/` subfolders:

```bash
ln -s /path/to/skills/plugins/engineering/skills/requirements-gap-analysis \
      ~/.config/opencode/skill/requirements-gap-analysis
```

## Using with VS Code (Copilot / Claude extensions)

If your VS Code extension supports the Agent Skills format, copy or symlink the skill folder into the extension's configured skills path. Check your extension's docs for the exact setting name (e.g. GitHub Copilot's custom instructions/skills folder, or the Claude Code VS Code extension, which shares Claude Code's `~/.claude/skills/` directory).

## Adding a new skill

1. If the category doesn't exist yet, create its plugin manifest at `plugins/<category>/.claude-plugin/plugin.json`:
   ```json
   {
     "name": "category-name",
     "displayName": "Human Readable Category",
     "description": "What this category of skills covers.",
     "version": "1.0.0",
     "author": { "name": "Rodrigo Azevedo", "email": "razevedo.contato@gmail.com" },
     "license": "MIT"
   }
   ```
   and register it in `.claude-plugin/marketplace.json` with a `source` of `./plugins/<category>`.
2. Add the skill at `plugins/<category>/skills/<skill-name>/SKILL.md`:
   ```yaml
   ---
   name: skill-name
   description: >
     When to use this skill, phrased so the assistant can match it against
     user requests.
   version: 1.0.0
   ---
   ```
   Write the workflow instructions in the body, and add supporting files under `references/` (loaded on demand) or `evals/` (test fixtures/cases).
3. Bump the category plugin's `version` in both `plugins/<category>/.claude-plugin/plugin.json` and its entry in `.claude-plugin/marketplace.json` so existing installs pick up the new skill on update.

## License

MIT — see [LICENSE](LICENSE).
