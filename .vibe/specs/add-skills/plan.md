# Implementation Plan: Agent Skills for cur8d Lambda

Establish structured Agent Skills in `cur8d/lambda` so AI coding agents can reliably build, extend, and verify AWS Lambda solutions and CDK infrastructure.

## Proposed Changes

### Skills Scaffolding

#### [NEW] `.agents/skills/add-lambda-handler/SKILL.md`
- Provide actionable instructions for creating new Lambda handlers with Powertools (Logger, Tracer, Metrics), Pydantic validation, structured responses, and unit tests.

#### [NEW] `.agents/skills/add-cdk-stack/SKILL.md`
- Provide step-by-step guidance for adding and wiring new CDK stacks under `infra/stacks/` and connecting them to `infra/app.py`.

#### [NEW] `.agents/skills/local-invoke/SKILL.md`
- Provide instructions for generating synthetic event payloads and testing execution via LocalStack.

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
