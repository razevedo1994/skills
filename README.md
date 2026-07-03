# Personal Skills

A personal collection of [Agent Skills](https://code.claude.com/docs/en/skills) — reusable, model-invoked instructions that extend coding assistants with specialized workflows.

This repo is a Claude Code **plugin marketplace** (`.claude-plugin/marketplace.json`): every skill lives in its own plugin under `plugins/`, so you can install just the ones you want instead of pulling in the whole collection.

```
.claude-plugin/
  marketplace.json                       # lists every plugin in this repo
plugins/
  requirements-gap-analysis/
    .claude-plugin/plugin.json           # this plugin's manifest
    skills/
      requirements-gap-analysis/
        SKILL.md                         # find gaps between docs and code
        references/
        evals/
```

Each skill folder contains a `SKILL.md` with YAML frontmatter (`name`, `description`) plus the instructions, and optional `references/` or `evals/` subfolders with supporting material.

## Using with Claude Code

**Install a single plugin from the marketplace (recommended)**

1. Add this repo as a marketplace:
   ```
   /plugin marketplace add /path/to/skills
   ```
   Or, once published, `/plugin marketplace add <owner>/<repo>` or a Git/HTTPS URL.
2. Install just the plugin(s) you want:
   ```
   /plugin install requirements-gap-analysis@personal-skills
   ```
3. Restart or reload Claude Code. Run `/plugin marketplace update personal-skills` later to pick up new/updated skills.

Browse everything on offer with `/plugin` or `/plugin marketplace list`.

**As a loose skill (no plugin install)**

Copy or symlink an individual skill folder into one of Claude Code's skill directories:

- Personal, all projects: `~/.claude/skills/<skill-name>/`
- Project-local: `<project>/.claude/skills/<skill-name>/`

```bash
ln -s /path/to/skills/plugins/requirements-gap-analysis/skills/requirements-gap-analysis \
      ~/.claude/skills/requirements-gap-analysis
```

**Invoking a skill**

Skills are invoked automatically when your prompt matches their `description`, or explicitly with `/skill-name` (e.g. `/requirements-gap-analysis`).

## Using with Zed

Zed supports Agent Skills the same way Claude Code does. Symlink or copy a skill folder into Zed's skills directory (`~/.config/zed/skills/` or the project's `.zed/skills/`), matching the `<skill-name>/SKILL.md` layout above. See Zed's agent documentation for the exact directory in your installed version, since this has moved across releases.

## Using with opencode

opencode reads skills from `~/.config/opencode/skill/<skill-name>/SKILL.md` (global) or `.opencode/skill/<skill-name>/SKILL.md` (per-project). Copy or symlink a skill folder in, preserving its `SKILL.md` and any `references/`/`evals/` subfolders:

```bash
ln -s /path/to/skills/plugins/requirements-gap-analysis/skills/requirements-gap-analysis \
      ~/.config/opencode/skill/requirements-gap-analysis
```

## Using with VS Code (Copilot / Claude extensions)

If your VS Code extension supports the Agent Skills format, copy or symlink the skill folder into the extension's configured skills path. Check your extension's docs for the exact setting name (e.g. GitHub Copilot's custom instructions/skills folder, or the Claude Code VS Code extension, which shares Claude Code's `~/.claude/skills/` directory).

## Adding a new skill

1. Create a new plugin directory: `plugins/<skill-name>/.claude-plugin/plugin.json`
   ```json
   {
     "name": "skill-name",
     "displayName": "Human Readable Name",
     "description": "What this skill does and when it's used.",
     "version": "1.0.0",
     "author": { "name": "Rodrigo Azevedo", "email": "razevedo.contato@gmail.com" },
     "license": "MIT"
   }
   ```
2. Add the skill itself at `plugins/<skill-name>/skills/<skill-name>/SKILL.md`:
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
3. Register the plugin in `.claude-plugin/marketplace.json`, adding an entry to `plugins` with a matching `name`, `source` (`./plugins/<skill-name>`), `description`, and `version`.

## License

MIT — see [LICENSE](LICENSE).
