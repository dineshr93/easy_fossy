---
name: fossy
description: Secure API wrapper for easy_fossy library with token management for AI subagents
category: security
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, token-management, easy-fossy, ai-skills]
    related_skills: [kanban-orchestrator, kanban-worker]
---

# Fossy — Secure EasyFossy Wrapper for AI Skills

> Securely manage and use easy_fossy library within AI subagents. Handles token encryption, environment variables, automatic rotation, and audit logging before and after delegating to AI workers.

## Overview

This skill wraps the [easy_fossy](https://github.com/dineshr93/easy_fossy) Python library to provide secure token handling for AI subagents. It ensures tokens are never exposed in logs, handles rotation before task delegation, and maintains audit trails for compliance.

## Prerequisites

```bash
pip install easy-fossy requests cryptography
```

## Installation

```bash
pip install easy-fossy-secure
```

## Secure Token Configuration

### Method 1: Environment Variables (Production - Recommended)

```python
import os
from easy_fossy_secure import set_fossy_tokens

set_fossy_tokens({
    "FOSSY_TEST_URL": "http://fossology-test.com:8080/repo/api/v1/",
    "FOSSY_TEST_UNAME": "",
    "FOSSY_TEST_ACCESS": "write",
    "FOSSY_TEST_BEARER_TOKEN": "Bearer YOUR_TOKEN_HERE",
    "FOSSY_TEST_TOKEN_EXPIRE": "2026-12-31",
})
```

### Method 2: Encrypted Config File

```python
from easy_fossy_secure import config_with_encrypted_tokens

config = config_with_encrypted_tokens(
    filename="/home/dinesh/.fossy/config.ini",
    server="test",
    bearer_token=os.environ["FOSSY_TEST_BEARER_TOKEN"],
    encryption_key="your_32-char-encryption-key"
)
```

### Method 3: Token Vault

```python
from secure_token_vault import TokenVault

vault = TokenVault(vault_path="/home/dinesh/.local/share/fossy-tokens")

fossy_token = vault.load_token("fossy-test-token")
vault.log_access(token="fossy-test-token", user="current_user")
```

## Auto-Rotate Before AI Task

```python
from easy_fossy_secure import auto_rotate_if_needed

auto_rotate_if_needed(server="test", threshold_hours=24)
```

## Security Best Practices

✅ Never hardcode tokens in code  
✅ Use environment variables in production  
✅ Encrypt configs at rest  
✅ Rotate tokens before AI delegation  
✅ Audit token access  

## Author: Dinesh Ravi
## License: MIT
## GitHub: https://github.com/dineshr93/easy_fossy
## PyPI: easy-fossy-secure