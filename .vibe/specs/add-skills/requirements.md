# Requirements: Agent Skills for cur8d Lambda

## Overview

Equip the `cur8d/lambda` repository with modular Agent Skills following the open standard (compatible with `skills.sh`, Claude Code, Cursor, GitHub Copilot, and Google Antigravity). These skills enable AI agents to autonomously initialize new projects from this template, scaffold new event-driven Lambda functions with CDK stacks, invoke them locally via LocalStack, and deploy to AWS.

## User Goals

1. Enable developers and AI agents to initialize a new standalone Lambda service repository from this template with customized project name, description, and repository configuration.
2. Enable agents to scaffold new event handlers (API Gateway, SQS, EventBridge, S3, DynamoDB) adhering to cur8d's AWS Lambda Powertools conventions, Pydantic validation models, and automated tests.
3. Enable agents to invoke and test handlers locally using LocalStack (`mise run local:deploy`, `mise run local:up`).
4. Enable agents to safely synthesize, diff, and deploy CDK stacks to live AWS cloud accounts (`mise run diff`, `mise run deploy`).
5. Support distribution via `npx skills add cur8d/lambda` and project-level discovery under `.agents/skills/`.

## Functional Requirements

1. **`init-project` Skill**:
   - Location: `.agents/skills/init-project/SKILL.md`
   - Guides the agent through customizing the template into a new standalone repository.
   - Runs `uv run python scripts/init.py` (or prompts for project name, description, author).
   - Resets git remotes if forked, updates `pyproject.toml`, `infra/app.py`, and documentation.
   - Sets up `.env.local` from `.env.local.example`.

2. **`new-lambda` Skill**:
   - Location: `.agents/skills/new-lambda/SKILL.md`
   - Guides the agent to scaffold a complete new Lambda service:
     - Generates handler under `templates/<name>/handler.py` with AWS Lambda Powertools (`Logger`, `Tracer`, `Metrics`).
     - Generates settings and Pydantic models under `templates/<name>/settings.py` and `models.py`.
     - Generates matching CDK infrastructure stack under `infra/stacks/<name>.py` and registers it in `infra/app.py`.
     - Generates comprehensive unit tests under `tests/<name>/test_handler.py`.
     - Can invoke `uv run python scripts/new.py --name <name>`.

3. **`local-invoke` Skill**:
   - Location: `.agents/skills/local-invoke/SKILL.md`
   - Instructions to create synthetic event payloads and test local Lambda invocation.
   - Guides the agent to start LocalStack (`mise run local:up`), deploy stack locally (`mise run local:deploy <stack>`), and invoke handler.

4. **`deploy-aws` Skill**:
   - Location: `.agents/skills/deploy-aws/SKILL.md`
   - Step-by-step guidance for deploying stacks to live AWS cloud:
     1. Verify credentials and target AWS region (`aws sts get-caller-identity`).
     2. Run `mise run verify` to ensure tests and linters pass before deployment.
     3. Inspect changes via `mise run diff <stack>`.
     4. Deploy via `mise run deploy <stack>`.
     5. Verify deployment health and cloud outputs.

5. **Integration & Discoverability**:
   - Update `AGENTS.md` and `docs/README.md` to document the available skills and how to run them with `npx skills`.

## Non-Functional Requirements

- All skills must include valid YAML frontmatter (`name`, `description`, `category`, `tags`).
- Descriptions must be trigger-rich and action-oriented for progressive disclosure.
- Must keep each `SKILL.md` file concise (under 500 lines).
- Must adhere strictly to existing repository validation (`mise run verify` must pass).
