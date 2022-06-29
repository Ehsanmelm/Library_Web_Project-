# *****************imports*****************
from cgitb import html
import json
from re import template
from unicodedata import name
from fastapi import FastAPI, Request, Response, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from numpy import choose
from prompt_toolkit import HTML
from requests import request
# ******************************************

webapp = FastAPI()
templates = Jinja2Templates(directory="templates/")

# **********************ROOT*****************


@webapp.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("root.htm", context={"request": request})
