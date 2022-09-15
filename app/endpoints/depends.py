from app.db.base import database
from app.repositories.items import ItemRepository


def get_item_repository() -> ItemRepository:
    return ItemRepository(database)
