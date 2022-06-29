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

# ********************************************
# ******************Give Info******************


@webapp.get("/Add memeber", response_class=HTMLResponse)
def add_member(request: Request):
    return templates.TemplateResponse("AddUser.htm", context={"request": request, "msg": ""})


@webapp.post("/save_users_info", response_class=HTMLResponse)
def save_users_info(request: Request, name=Form(...), pas=Form(...), confirm_pass=Form(...)):
    name = name.lower()
    with open("users.json", "r") as js_file:
        user_dict = json.load(js_file)
    if(pas == confirm_pass):
        user_dict[name] = pas
        with open("users.json", "w") as js_file:
            json.dump(user_dict, js_file)
        return templates.TemplateResponse("AddUser.htm", context={"request": request, "msg": f"*****user {name} added*****"})

    else:
        return templates.TemplateResponse("AddUser.htm", context={"request": request, "msg": "*******confirm password isnot correct*******"})
