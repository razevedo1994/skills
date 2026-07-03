# CLAUDE.md

This repo is a Claude Code plugin marketplace of personal Agent Skills, grouped by category (one plugin per category under `plugins/<category>/`). See `README.md` for the full layout, installation instructions, and end-user docs.

## Creating or editing a skill

1. **Read `plugins/productivity/skills/writing-great-skills/SKILL.md` first** (and its `GLOSSARY.md`) — it is the house style for what makes a skill predictable: invocation choice, information hierarchy, pruning, leading words, failure modes. Every new or edited skill must follow it. It is user-invoked only, so load it explicitly rather than expecting it to fire on its own.
2. Follow the "Adding a new skill" steps in `README.md` for the mechanics: where the plugin manifest and `SKILL.md` live, the frontmatter shape, and bumping the category plugin's `version` in both `plugins/<category>/.claude-plugin/plugin.json` and its entry in `.claude-plugin/marketplace.json`.
3. After writing or editing a skill, review it against `writing-great-skills` explicitly — check the description for no-op boilerplate and duplicated trigger branches, check the body for duplication between `SKILL.md` and any disclosed `references/*.md`, and confirm each step has a checkable completion criterion.
4. Update `README.md`'s "Available skills" table with the new skill's category, name, and one-line description.
5. If the skill includes `evals/`, keep `evals/evals.json` prompts and expectations in sync with any behavior changes.

## Conventions

- One skill per folder: `plugins/<category>/skills/<skill-name>/SKILL.md`, kebab-case name matching the `name:` frontmatter field.
- Push reference material the agent doesn't need on every run into `references/` and link to it with a context pointer from `SKILL.md` — don't inline everything.
- Don't create a new category/plugin for one skill unless it doesn't fit an existing category; category descriptions in `.claude-plugin/marketplace.json` should stay accurate as their skill sets grow.
