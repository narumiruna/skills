---
name: using-peewee-orm
description: Deprecated internal reference for designing, wiring, or testing Peewee ORM models with deferred database binding, scoped connections, explicit transactions, and isolated SQLite fixtures.
metadata:
  internal: true
---

# Python Peewee (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility. Bind models at an application or test boundary; keep connection lifetime, transaction lifetime, and schema lifecycle explicit.

## Model Setup

```python
from peewee import DatabaseProxy, Model, SqliteDatabase

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


db = SqliteDatabase("app.db", pragmas={"foreign_keys": 1})
db_proxy.initialize(db)
```

Define one proxy and base model for a connected model graph. Do not bind production credentials or open a production connection at import time.

## Lifecycle Rules

- Use `db.connection_context()` when a function owns a scoped open/close boundary.
- Use `db.atomic()` for multiple statements that must commit or roll back as one invariant. A transaction is not a substitute for deciding who owns the connection.
- Pass or retain the initialized database handle at the boundary instead of reaching through private proxy internals.
- Initialize the proxy before querying. Avoid process-long connections unless the application architecture deliberately owns them.
- Do not run schema changes, table deletion, migrations, or writes against an external or production database without explicit authorization for that target and operation.

```python
with db.connection_context():
    rows = list(User.select().limit(100))

with db.connection_context():
    with db.atomic():
        account.debit(amount)
        ledger.record(account, amount)
```

## Isolated SQLite Tests

Keep one deterministic model list and guarantee cleanup:

```python
import pytest
from peewee import SqliteDatabase

MODELS = [User]


@pytest.fixture
def test_db(tmp_path):
    db = SqliteDatabase(
        str(tmp_path / "test.db"),
        pragmas={"foreign_keys": 1},
    )
    db_proxy.initialize(db)
    try:
        with db.connection_context():
            db.create_tables(MODELS)
        yield db
    finally:
        with db.connection_context():
            db.drop_tables(MODELS, safe=True)
```

A temporary file-backed database preserves its schema when tested code owns and closes scoped connections. Exercise at least two sequential `connection_context()` blocks—such as a write followed by a read—and test rollback behavior for multi-statement invariants. Do not reuse an application database or depend on table state from another test.

Finish by reporting the binding boundary, connection and transaction ownership, schema-test lifecycle, and checks run.
