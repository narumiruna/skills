# Logging with Loguru

Use Loguru when an app or CLI owns process startup and logging configuration. Reusable libraries should normally emit stdlib logging records instead.

## Install and Configure

```bash
uv add loguru
```

Configure sinks once near the application entry point:

```python
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message} | {extra}",
    level="INFO",
    diagnose=False,
)
```

Disable exception-variable diagnostics to keep local values out of logs.
Add file or external sinks only when the application requires them. Consider retention, sensitive fields, destination approval, and duplicate setup.

## Context

Bind structured context so it is present in `{extra}` (or use `serialize=True` for JSON):

```python
request_logger = logger.bind(user_id=123, action="login")
request_logger.info("User action")
```

## Exceptions

Log and propagate unexpected exceptions unless the caller deliberately owns recovery:

```python
from loguru import logger


@logger.catch(reraise=True)
def risky_function(x: int) -> float:
    return 1 / x
```

For an intentionally handled exception, use an explicit `try`/`except`, log with `logger.exception(...)`, and return or raise according to the documented recovery behavior.
