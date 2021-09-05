import re
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from pathlib import Path

import url_checker

shareVideoHostingApi = FastAPI()

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

@shareVideoHostingApi.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:

        data = await websocket.receive_text()

        await websocket.send_text(f"Message text was: {data}")
