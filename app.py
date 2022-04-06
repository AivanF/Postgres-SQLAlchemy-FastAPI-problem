__author__ = "AivanF"

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import async_session, create_database, create_object, get_objects

app = FastAPI()
some_items = dict()


@app.on_event("startup")
async def startup():
    await create_database()
    # Extract some data from env, local files, or S3
    some_items["pi"] = 3.1415926535
    some_items["eu"] = 2.7182818284


@app.post("/{name}")
async def create_obj(name: str, request: Request):
    data = await request.json()
    if data.get("code") in some_items:
        data["value"] = some_items[data["code"]]
        async with async_session() as session:
            async with session.begin():
                await create_object(session, name, data)
        return JSONResponse(status_code=200, content=data)
    else:
        return JSONResponse(status_code=404, content={})


@app.get("/{name}")
async def get_connected_register(name: str):
    async with async_session() as session:
        async with session.begin():
            objects = await get_objects(session, name)
    result = []
    for obj in objects:
        result.append({
            "id": obj.id,
            "name": obj.name,
            **obj.data,
        })
    return result


if __name__ == '__main__':
    uvicorn.run("app:app", port=4321, host="0.0.0.0")
