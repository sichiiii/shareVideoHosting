import re
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from pathlib import Path
from connection_manager import ConnectionManager

import url_checker

shareVideoHostingApi = FastAPI()
manager = ConnectionManager()

shareVideoHostingApi.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="templates")

directory=Path(__file__).parent.parent.absolute() 

@shareVideoHostingApi.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@shareVideoHostingApi.post("/watch")
async def watch(request: Request, url: str = Form(...)):
    urlCheckerObject = url_checker.Url_Checker(url)
    final_url = urlCheckerObject.get_url()
    return templates.TemplateResponse("watch.html", {"request": request, "url" : final_url})
    
@shareVideoHostingApi.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'pause':
                print('pause')
            elif data == 'start':
                print('start')
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
