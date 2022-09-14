from .base import metadata, engine
from .items import items

metadata.create_all(bind=engine)
