from fastapi import APIRouter, Depends
from app.endpoints.depends import get_item_repository
from app.models.item import ImportItems
from app.repositories.items import ItemRepository

router = APIRouter()


@router.get("/nodes/{id}")
async def import_item(
        id: str,
        items: ItemRepository = Depends(get_item_repository)):
    return await items.get_item_by_id(id=id)


@router.post("/import")
async def import_item(
        item: ImportItems,
        items: ItemRepository = Depends(get_item_repository)):
    return await items.adding_item(add=item)


@router.delete("/delete/{id}")
async def delete_item(
        id: str,
        date: str,
        items: ItemRepository = Depends(get_item_repository)):
    return await items.delete_item(id=id)
