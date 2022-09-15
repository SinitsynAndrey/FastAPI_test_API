from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MyEnum(str, Enum):
    file = 'FILE'
    folder = 'FOLDER'


class Item(BaseModel):
    id: str
    url: str | None
    date: datetime
    parentId: str | None
    type: MyEnum
    size: int | None


class NodeItem(BaseModel):
    id: str
    url: str | None
    type: str
    parentId: str | None
    size: int | None
    date: datetime
    children: list


class ImportItemFile(BaseModel):
    id: str
    url: str
    parentId: str
    size: int
    type: MyEnum


class ImportItemFolder(BaseModel):
    id: str
    parentId: str | None
    type: MyEnum


class ImportItems(BaseModel):
    items: list
    updateDate: datetime
