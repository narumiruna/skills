---
name: configuring-python-logging
description: Deprecated internal reference for choosing, configuring, or reviewing Python logging for libraries, services, apps, and CLIs, including stdlib logging, Loguru, handlers, levels, context, and exception behavior.
metadata:
  internal: true
---

# Python Logging (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility. Choose the logging boundary before choosing syntax.

## Decision

- Use stdlib `logging` for reusable libraries, long-lived services, mixed ecosystems, and standard Sentry/OpenTelemetry or handler integration.
- Consider Loguru for a small app or CLI that owns process startup and the full logging surface.
- In mixed systems, keep libraries on stdlib logging and let the application own any deliberate bridge.

## Workflow

1. Inspect the existing logging stack, entry points, deployment environment, and operational integrations.
2. Keep libraries passive: create `logging.getLogger(__name__)`; do not configure process-wide handlers or levels during import.
3. Configure logging once at the app or CLI boundary. Prevent duplicate handlers or sinks when setup can run repeatedly.
4. Set levels and formats for the actual audience. Add structured fields at a defined boundary and provide defaults when third-party records use the same formatter.
5. Preserve exception semantics: log tracebacks without silently swallowing failures unless recovery is intentional and tested.
6. Add file, network, telemetry, or other data-egress sinks only when requested or already established by project policy; external destinations require explicit authorization and secret-safe configuration.
7. Exercise representative application, library, third-party, and exception records. Report the backend chosen, configuration boundary, checks run, and any integration caveat.

## Focused References

- Read `references/logging.md` for stdlib logger, handler, context, and exception patterns.
- Read `references/loguru.md` only when the application owns Loguru configuration.

Do not mix backends without an explicit ownership and interoperability plan, hide global setup in imported modules, or add sinks inside repeatedly called functions.
