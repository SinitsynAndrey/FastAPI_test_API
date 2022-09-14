from db.items import items
from models.item import Item, ImportItems, ImportItemFile, ImportItemFolder
from .base import BaseRepository


class ItemRepository(BaseRepository):

    async def get_item_by_id(self, id: str) -> dict:
        query = items.select().where(items.c.id == id)
        item = await self.database.fetch_one(query)
        if item:
            i_p = Item.parse_obj(item)
            if i_p.type == "FILE":
                children = None
            else:
                children = await self.get_children_item(id)
            values = {**i_p.dict()}
            values.pop("date", None)
            return {**values, 'date': item['date'].strftime('%Y-%m-%dT%H:%M:%SZ'), 'children': children}
        return {"code": 404, "message": "Item not found"}

    async def get_children_item(self, id: str) -> list[dict] | None:
        query = items.select().where(items.c.parentId == id)
        children_all = await self.database.fetch_all(query)
        if not children_all:
            return []
        children_list = []
        for child in children_all:
            child_p = Item.parse_obj(child)
            if child_p.type == "FILE":
                children = None
            else:
                children = await self.get_children_item(child_p.id)
            values = {**child_p.dict()}
            values.pop("date", None)
            children_list.append({**values, 'date': child['date'].strftime('%Y-%m-%dT%H:%M:%SZ'), 'children': children})
        return children_list

    async def update_parent_size(self, id: str, size: int) -> None:

        query = items.select().where(items.c.id == id)
        parent = await self.database.fetch_one(query)
        values = {**parent}
        values['size'] += size
        query = items.update().where(items.c.id == id).values(values)
        await self.database.execute(query=query)
        if parent.parentId:
            await self.update_parent_size(parent.parentId, size)

    async def adding_item(self, add: ImportItems) -> dict:
        for add_item in add.dict()['items']:
            if add_item['type'] == "FOLDER":
                item = ImportItemFolder(
                    id=add_item['id'],
                    type=add_item['type'],
                    parentId=add_item['parentId'],
                )

                values = {**item.dict(),
                          'size': 0,
                          'date': add.dict()['updateDate']}
            else:
                item = ImportItemFile(
                    id=add_item['id'],
                    url=add_item['url'],
                    type=add_item['type'],
                    parentId=add_item['parentId'],
                    size=add_item['size'],
                )

                values = {**item.dict(), 'date': add.dict()['updateDate']}

            query = items.select().where(items.c.id == item.id)
            exist_item = await self.database.fetch_one(query)

            if exist_item:
                if item.type == 'FOLDER':
                    values['size'] = exist_item['size']
                if item.parentId and values['size'] - exist_item['size'] != 0:
                    await self.update_parent_size(item.parentId, values['size'] - exist_item['size'])
                query = items.update().where(items.c.id == item.id).values(**values)
            else:
                if item.parentId and values['size'] > 0:
                    await self.update_parent_size(item.parentId, values['size'])
                query = items.insert().values(**values)
            await self.database.execute(query=query)

        return {"code": 200, "message": "Вставка или обновление прошли успешно."}

    async def delete_item(self, id: str):
        query = items.select().where(items.c.id == id)
        item = await self.database.fetch_one(query)
        if item:
            query = items.delete().where(items.c.id == id)
            await self.database.execute(query=query)
            return {"code": 200, "message": "Удаление успешно прошло"}
        return {"code": 404,  "message": "Item not found"}
