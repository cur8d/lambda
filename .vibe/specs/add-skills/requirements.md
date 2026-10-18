# Requirements: Agent Skills for cur8d Lambda

## Overview

Equip the `cur8d/lambda` repository with modular Agent Skills following the open standard (compatible with `skills.sh`, Claude Code, Cursor, GitHub Copilot, and Google Antigravity). These skills enable AI agents to autonomously scaffold, test, and deploy Lambda event handlers and CDK infrastructure according to cur8d architecture patterns.

## User Goals

1. Enable developers and AI agents to quickly scaffold new Lambda handlers (API Gateway, SQS, EventBridge, S3, DynamoDB Stream) adhering to cur8d's AWS Lambda Powertools conventions and Pydantic validation.
2. Enable agents to generate matching CDK infrastructure stacks under `infra/stacks/` and register them in `infra/app.py`.
3. Provide local invocation and verification skills utilizing LocalStack and `mise` tasks (`mise run local:deploy`, `mise run verify`).
4. Support distribution via `npx skills add cur8d/lambda` and project-level discovery under `.agents/skills/`.

## Functional Requirements

1. **`add-lambda-handler` Skill**:
   - Location: `.agents/skills/add-lambda-handler/SKILL.md`
   - Instructions for the agent to scaffold a new handler under `templates/<event_type>/` or custom handler path.
   - Must mandate AWS Lambda Powertools (`Logger`, `Tracer`, `Metrics`).
   - Must mandate typed event models via Pydantic (`models.py`) and standard JSON responses.
   - Must scaffold unit tests in `tests/test_<handler>.py` covering successful execution, invalid payloads, and error handling.

2. **`add-cdk-stack` Skill**:
   - Location: `.agents/skills/add-cdk-stack/SKILL.md`
   - Instructions for the agent to scaffold a CDK stack in `infra/stacks/<type>_stack.py`.
   - Wires appropriate triggers (e.g. SQS queue, API Gateway REST/HTTP API, EventBridge bus rule, DynamoDB stream).
   - Configures environment variables, least-privilege IAM policies, and registers the stack into `infra/app.py`.

3. **`local-invoke` Skill**:
   - Location: `.agents/skills/local-invoke/SKILL.md`
   - Instructions to create synthetic event payloads and test local Lambda invocation.
   - Guides the agent to spin up LocalStack via `mise run local:up`, deploy with `mise run local:deploy <stack>`, and invoke using AWS CLI or local invoke scripts.

4. **Integration & Discoverability**:
   - Update `AGENTS.md` and `docs/README.md` to document the available skills and how to run them with `npx skills`.
   - Add a mise task `mise run skills:list` or verify skills discoverability via `npx skills`.

## Non-Functional Requirements

- All skills must include valid YAML frontmatter (`name`, `description`, `category`, `tags`).
- Descriptions must be trigger-rich and action-oriented for progressive disclosure.
- Must keep each `SKILL.md` file concise (under 500 lines).
- Must adhere strictly to existing repository validation (`mise run verify` must pass).
