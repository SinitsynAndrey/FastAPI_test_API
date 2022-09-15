from fastapi import FastAPI
import uvicorn

from app.db.base import database
from app.endpoints import items

app = FastAPI(title='Enrollment')
app.include_router(items.router, tags=['items'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
