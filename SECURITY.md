# Security Policy

## Scope

This repository distributes Claude Code plugins composed of markdown prompts,
JSON manifests, and a shell hook. The most relevant risks are in the
[`hooks/hooks.json`](plugins/agentic-engineering/hooks/hooks.json) commands (which
run on the user's machine) and any shell snippets in skill references. Reports
about those, or about anything that could cause a plugin to take an unsafe action,
are especially welcome.

## Supported versions

The latest released version on the default branch (`main`) is supported. There are
no backported fixes for older tags — fixes land in a new release.

## Reporting a vulnerability

**Please do not open a public issue for a security problem.**

Use GitHub's private reporting instead:
[**Report a vulnerability**](https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/security/advisories/new).
This opens a confidential advisory visible only to the maintainer.

Please include:

- a description of the issue and its impact,
- the file/command involved and steps to reproduce,
- any suggested remediation.

You can expect an acknowledgement within a few days. Once a fix is ready, it ships
in a new release and the advisory is published with credit (unless you prefer to
remain anonymous).
