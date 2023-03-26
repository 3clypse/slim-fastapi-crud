# SQLAlchemy models

from sqlalchemy import Table, Column, Integer, String

from database import metadata

users = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True),
    Column("gh_id", Integer),
    Column("username", String, nullable=False,
           unique=True, sqlite_on_conflict_unique='FAIL'),
    Column("first_name", String),
    Column("last_name", String),
    Column("address", String),
    Column("roles", String, nullable=False),
    sqlite_autoincrement=True
)
