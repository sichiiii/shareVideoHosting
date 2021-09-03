import re
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from pathlib import Path

import url_checker
import get_playback

shareVideoHostingApi = FastAPI()

shareVideoHostingApi.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="templates")

directory=Path(__file__).parent.parent.absolute() 
print(directory)

class Url(BaseModel):
    url : str

@shareVideoHostingApi.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@shareVideoHostingApi.post("/")
async def root(request: Request, url: str = Form(...)):
    urlCheckerObject = url_checker.Url_Checker(url)
    final_url = urlCheckerObject.get_url()[0]
    playbackObject = get_playback.Playback(final_url)
    playbackObject.get_playback()
    return templates.TemplateResponse("index.html", {"request": request})
    
