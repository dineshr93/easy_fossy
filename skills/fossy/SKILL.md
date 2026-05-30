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

> Securely manage and use easy_fossy library within AI subagents. Handles token authentication, config management, and Fossy API integration.

## Overview

This skill wraps the [easy_fossy](https://github.com/dineshr93/easy_fossy) Python library to integrate with AI workers. It handles common tasks for Fossy API access, token management, and secure configuration.

## Prerequisites

```bash
pip install easy-fossy requests
```

## Installation

```bash
# Install the actual easy-fossy package from PyPI
pip install easy-fossy

# IMPORTANT: The package "easy-fossy-secure" does NOT exist on PyPI!
# Only "easy-fossy" is available at https://pypi.org/project/easy-fossy/
