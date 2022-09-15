from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Table

from .base import metadata

items = Table(
    'items',
    metadata,
    Column('id', String, primary_key=True),
    Column('url', String, unique=True, nullable=True),
    Column('date', DateTime(timezone=True)),
    Column('parentId', String, ForeignKey('items.id', ondelete="CASCADE"), nullable=True),
    Column('type', String),
    Column('size', Integer),

)
