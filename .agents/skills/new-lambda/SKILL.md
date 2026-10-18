---
name: new-lambda
description: Scaffolds a new event-driven AWS Lambda function adhering to cur8d standards with Powertools (Logger, Tracer, Metrics), Pydantic models, unit tests, and CDK infrastructure stack. Use whenever the user asks to create, scaffold, or add a Lambda function or service.
category: coding
tags: [aws, lambda, cdk, python, powertools, cur8d]
---

# Create New Lambda Function in cur8d/lambda

This skill guides you through scaffolding, implementing, and registering a new AWS Lambda function and its corresponding AWS CDK infrastructure stack in `cur8d/lambda`.

## Prerequisites

- Python 3.12+ and `uv` installed
- `mise` installed
- Docker installed and running (for local test invoke via LocalStack)

## Workflow

### 1. Scaffold Boilerplate Files
Run the built-in generator script with the function name (in snake_case or kebab-case):

```bash
uv run python scripts/new.py --name <function_name>
```

This generates:
- `templates/<function_name>/handler.py` (Lambda handler entry point)
- `templates/<function_name>/models.py` (Pydantic payload/event models)
- `templates/<function_name>/settings.py` (Environment variables and settings via Pydantic)
- `tests/<function_name>/test_handler.py` (Pytest test suite)
- `infra/stacks/<function_name>.py` (AWS CDK Stack definition)
- `docs/template/<function_name>.md` & `docs/reference/<function_name>.md` (Documentation)
- Updates `infra/app.py` to register the new stack in `STACK_REGISTRY`.

### 2. Implement Handler Logic & Models
In `templates/<function_name>/handler.py`:
- Use AWS Lambda Powertools decorators:
  ```python
  from aws_lambda_powertools import Logger, Metrics, Tracer

  logger = Logger()
  tracer = Tracer()
  metrics = Metrics()


  @logger.inject_lambda_context(log_event=True)
  @tracer.capture_lambda_handler
  @metrics.log_metrics(capture_cold_start_metric=True)
  def lambda_handler(event: dict, context) -> dict: ...
  ```
- Define typed request/event models in `models.py` using Pydantic.
- Define environment settings in `settings.py` using `pydantic_settings.BaseSettings`.

### 3. Configure the CDK Stack
In `infra/stacks/<function_name>.py`:
- Customize runtime settings (memory size, timeout, log retention).
- Wire triggers according to event source (API Gateway, SQS Queue, S3 Event, EventBridge rule, DynamoDB Streams).
- Configure IAM permissions with least privilege.

### 4. Implement Unit Tests
In `tests/<function_name>/test_handler.py`:
- Test successful execution with nominal mock event payloads.
- Test invalid event schemas (expect appropriate validation errors).
- Test error handling and cold start resilience.

### 5. Verify Quality Gates
Run repository verification:

```bash
mise run verify
```

Ensure formatting (`ruff format`), linting (`ruff check`), type checks, and pytest tests pass.

## Boundaries

✅ **Always do:**
- Always decorate handlers with `@logger.inject_lambda_context`, `@tracer.capture_lambda_handler`, and `@metrics.log_metrics`.
- Always register the new CDK stack in `infra/app.py`'s `STACK_REGISTRY`.
- Always verify all checks pass with `mise run verify` before committing.

🚫 **Never do:**
- Never hardcode AWS credentials, account IDs, or region names in handlers or stacks.
- Never write handlers without companion unit tests in `tests/<function_name>/`.
