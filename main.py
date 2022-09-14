from fastapi import FastAPI
import uvicorn

from db.base import database
from endpoints import items

app = FastAPI(title='Enrollment')
app.include_router(items.router, tags=['items'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080)
