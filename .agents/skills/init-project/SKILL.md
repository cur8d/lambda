---
name: init-project
description: Initializes and customizes a new AWS Lambda service repository from the cur8d/lambda template. Use whenever the user asks to initialize, bootstrap, or configure a newly cloned or forked Lambda project.
category: system
tags: [scaffolding, template, init, aws, lambda, cur8d]
---

# Initialize Project from cur8d/lambda Template

This skill guides you through transforming a newly cloned or forked `cur8d/lambda` repository into a fully personalized, standalone AWS Lambda project.

## Prerequisites

- Python 3.12+ and `uv` installed
- `mise` installed
- Clean git working tree

## Workflow

### 1. Gather Project Parameters
Identify or ask the user for:
- **Project Name** (kebab-case, e.g., `billing-service`)
- **Description** (one-line summary, e.g., `Billing webhook and subscription processor`)
- **Author Name** and **Email** (fallback to current git user: `git config user.name`, `git config user.email`)
- **GitHub Username / Org** (e.g., `cur8d` or your personal handle)

### 2. Execute Template Initialization
Run the built-in initialization script using `uv`:

```bash
uv run python scripts/init.py \
  --name "<project-name>" \
  --description "<project-description>" \
  --author "<author-name>" \
  --email "<author-email>" \
  --github "<github-username>"
```

The script will:
- Rename `templates/` to the sanitized project package name (e.g. `billing_service/`).
- Update package metadata in `pyproject.toml`.
- Update repository references in `mkdocs.yml`, `.github/CODEOWNERS`, and documentation.
- Remove `scripts/init.py` upon successful customization.

### 3. Local Environment Configuration
Copy the template local environment file:

```bash
cp .env.local.example .env.local
```

Instruct the user or configure `LOCALSTACK_AUTH_TOKEN` if using LocalStack Pro features.

### 4. Verify Baseline
Run repository verification to ensure formatting, linting, and tests pass:

```bash
mise run verify
```

## Boundaries

✅ **Always do:**
- Always run `mise run verify` after initialization to ensure all renamed imports resolve cleanly.
- Always verify git config values before prompting the user for author information.
- Always copy `.env.local.example` to `.env.local`.

🚫 **Never do:**
- Never run the initialization script with empty or invalid names (only alphanumeric characters, dashes, and underscores are allowed).
- Never push initial changes to the upstream `cur8d/lambda` template repo; ensure git remotes point to the user's repository.
