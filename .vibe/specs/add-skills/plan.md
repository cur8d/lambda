# Implementation Plan: Agent Skills for cur8d Lambda

Establish structured Agent Skills in `cur8d/lambda` so AI coding agents can reliably initialize projects from the template, build and test new event-driven Lambda functions, invoke them locally, and deploy to AWS.

## Proposed Changes

### Skills Scaffolding

#### [NEW] `.agents/skills/init-project/SKILL.md`
- Instructions for customizing the template into a standalone service repository using `scripts/init.py`.

#### [NEW] `.agents/skills/new-lambda/SKILL.md`
- Instructions for scaffolding complete Lambda functions, tests, and CDK stacks using `scripts/new.py`.

#### [NEW] `.agents/skills/local-invoke/SKILL.md`
- Instructions for local testing and execution against LocalStack.

#### [NEW] `.agents/skills/deploy-aws/SKILL.md`
- Instructions for pre-flight verification, diffing, and deploying CDK stacks to AWS cloud.

---

### Documentation & Agents Guidance

#### [MODIFY] `AGENTS.md`
- Document the newly introduced skills under `.agents/skills/`.
- Provide guidance on using `npx skills add cur8d/lambda` or invoking skills directly.

#### [MODIFY] `docs/README.md`
- Add an "Agent Skills" section explaining how developers and agents can consume the repository's built-in skills.

---

### Verification Plan

#### Automated Verification
- Run `mise run verify` (linting with ruff, type checks, and pytest suite execution).
- Run `npx skills ls` to confirm skills are detected by the skills CLI.
