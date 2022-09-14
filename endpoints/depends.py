from db.base import database
from repositories.items import ItemRepository


def get_item_repository() -> ItemRepository:
    return ItemRepository(database)
