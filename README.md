# BlogUpdaterRoutine

This project uses Alembic for database schema versioning, allowing for easy management of database migrations.

## Managing Database Versioning with Alembic

Alembic is a lightweight database migration tool for use with SQLAlchemy.
It provides command line tools for creating and managing scriptable database revisions.

### Updating Database Versioning

To create a new migration script after modifying your SQLAlchemy models, run:

```bash
alembic revision --autogenerate -m "DESCRIPTION_HERE"
```

Then, when youcan apply the update using

```bash
alembic upgrade head
```
