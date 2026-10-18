---
name: deploy-aws
description: Synthesizes, diffs, and deploys CDK Lambda stacks to AWS cloud environments using mise and CDK CLI. Use whenever the user asks to deploy, diff, or release a Lambda stack to AWS.
category: coding
tags: [aws, cdk, deploy, cloud, lambda, cur8d]
---

# Deploy cur8d Lambda Stacks to AWS

This skill guides you through deploying AWS CDK Lambda stacks to a live AWS cloud environment adhering to cur8d quality and safety gates.

## Prerequisites

- AWS CLI configured with active credentials (`aws sts get-caller-identity` succeeds)
- `mise` installed
- Docker installed (required for CDK bundling and container image lambdas)

## Workflow

### 1. Verify Active AWS Identity & Target Environment
Verify credentials and current account/region:

```bash
aws sts get-caller-identity
```

Ensure `AWS_REGION` or `AWS_DEFAULT_REGION` is explicitly configured.

### 2. Pre-Flight Verification
Run all tests and linters before executing any cloud deployment:

```bash
mise run verify
```

Fix any linting or test regressions before proceeding.

### 3. Inspect CDK Infrastructure Changes (Diff)
Generate a diff against the currently deployed cloud stack:

```bash
mise run diff <stack_name>
```

Carefully inspect:
- Resources being added, updated, or destroyed (look out for accidental deletions of stateful resources like DynamoDB tables or S3 buckets).
- IAM permission changes and policies.

### 4. Deploy the Stack
Deploy the stack to AWS:

```bash
mise run deploy <stack_name>
```

Monitor the deployment progress in the terminal output. Upon success, CDK outputs (API Gateway endpoints, ARN outputs) will be printed.

### 5. Post-Deployment Verification
- Test the deployed Lambda or API Gateway endpoint using `curl` or AWS CLI.
- Check CloudWatch Logs for recent invocations:
  ```bash
  aws logs tail /aws/lambda/<function_name> --since 5m --follow
  ```

### 6. Teardown / Destruction (If Requested)
To tear down the deployed stack:

```bash
mise run destroy <stack_name>
```

## Boundaries

✅ **Always do:**
- Always run `aws sts get-caller-identity` to confirm the target account before deploying.
- Always run `mise run verify` and `mise run diff <stack_name>` prior to deployment.
- Always capture and report cloud deployment outputs (e.g., API Gateway URLs) back to the user.

🚫 **Never do:**
- Never run deployment if `mise run verify` fails.
- Never destroy production stacks without explicit user confirmation.
