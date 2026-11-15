# Python stdlib Logging

Use stdlib logging for reusable libraries, services, and applications that need standard ecosystem integration.

## Library Pattern

```python
import logging

logger = logging.getLogger(__name__)


def load_user(user_id: int) -> None:
    logger.info("Loading user", extra={"user_id": user_id})
```

Library modules should not call `basicConfig()` or attach process-wide handlers. Let the application own levels, formatting, and destinations.

## Application Boundary

Configure once near process startup:

```python
import logging
import sys

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(user_id)s | %(message)s",
        defaults={"user_id": "-"},
    )
)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)
```

Defaults prevent third-party records without custom context from failing formatting. For larger systems, add request context with a `LoggerAdapter`, filter, or structured handler at a defined boundary.

Add file, telemetry, or network handlers only when deployment requirements call for them. Guard setup that might run repeatedly so handlers are not duplicated.

## Exceptions

Preserve the active traceback:

```python
try:
    run_job()
except JobError:
    logger.exception("Job failed")
    raise
```

Suppress or recover only when the application deliberately owns that behavior and tests it.
