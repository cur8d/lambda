---
name: local-invoke
description: Generates synthetic event payloads and tests Lambda function execution locally using LocalStack. Use whenever the user asks to test, invoke, or debug a Lambda function or CDK stack locally.
category: coding
tags: [aws, lambda, localstack, testing, invoke, cur8d]
---

# Test and Invoke Lambda Locally with LocalStack

This skill guides you through spinning up LocalStack, deploying the target CDK stack locally, generating test event payloads, and invoking the Lambda function without hitting AWS cloud.

## Prerequisites

- Docker installed and running
- `.env.local` configured (copied from `.env.local.example`)
- `mise` installed

## Workflow

### 1. Start LocalStack
Launch the local AWS emulation container:

```bash
mise run local:up
```

Verify that the LocalStack gateway is responding at `http://localhost:4566`:

```bash
curl -s http://localhost:4566/_localstack/health | jq .
```

### 2. Deploy Stack to LocalStack
Deploy the target stack locally using `aws-cdk-local`:

```bash
mise run local:deploy <stack_name>
```

*(You can also use the shorthand alias `mise run local <stack_name>` or `dl <stack_name>`)*

### 3. Generate Event Payload
Synthesize a JSON test event matching the Lambda's trigger. For example:

**API Gateway HTTP Payload:**
```json
{
  "version": "2.0",
  "routeKey": "POST /items",
  "rawPath": "/items",
  "headers": {
    "content-type": "application/json"
  },
  "body": "{\"name\": \"sample-item\", \"value\": 42}",
  "isBase64Encoded": false
}
```

**SQS Message Payload:**
```json
{
  "Records": [
    {
      "messageId": "msg-12345",
      "body": "{\"action\": \"process\", \"id\": 1}",
      "eventSource": "aws:sqs"
    }
  ]
}
```

Save payload to a temporary file (e.g. `/tmp/event.json`).

### 4. Invoke the Function
Invoke using AWS CLI pointing to the local endpoint:

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name <function_name> \
  --payload fileb:///tmp/event.json \
  /tmp/response.json
```

Inspect the output:
```bash
cat /tmp/response.json
```

### 5. Teardown / Cleanup
When testing is complete:

```bash
# Tear down the stack
mise run local:destroy <stack_name>

# Stop LocalStack container
mise run local:down
```

## Boundaries

✅ **Always do:**
- Always ensure LocalStack is up before deploying or invoking (`mise run local:up`).
- Always pass `--endpoint-url=http://localhost:4566` when using AWS CLI for local testing.
- Always clean up temporary payload files.

🚫 **Never do:**
- Never commit secret API tokens or sensitive production data in test payload files.
- Never deploy to real AWS when local testing is intended.
