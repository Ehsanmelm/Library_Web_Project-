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

# ***********************************************
# *****************Remove member*****************


@webapp.get("/Rmove member", response_class=HTMLResponse)
def remove_member(request: Request):
    return templates.TemplateResponse("Rmove_Member.htm", context={"request": request, "remove_msg": ""})


@webapp.post("/user_removing_process", response_class=HTMLResponse)
def user_removing_process(request: Request, remove_name=Form(...), remove_pas=Form(...)):
    remove_name = remove_name.lower()
    with open("users.json", "r") as js_file:
        UsersInfo = json.load(js_file)
        if((remove_name in UsersInfo) and UsersInfo[remove_name] == remove_pas):
            UsersInfo.pop(remove_name)
            with open("users.json", "w") as js_file:
                json.dump(UsersInfo, js_file)

            return templates.TemplateResponse("Rmove_Member.htm", context={"request": request, "remove_msg": f"*****user {remove_name} Removed*****"})

        else:

            return templates.TemplateResponse("Rmove_Member.htm", context={"request": request, "remove_msg": "*******User not Found*******"})

# *********************************************
# *****************Show Book*******************


@webapp.get("/Books list", response_class=HTMLResponse)
def show_book(request: Request):

    with open("Books.json") as js_file:
        Books_Info = json.load(js_file)

    return templates.TemplateResponse("ShowBooks.htm", context={"request": request, "Show_book": Books_Info})

# *********************************************
# ****************Remove Book******************


@webapp.get("/remove book", response_class=HTMLResponse)
def remove_Book(request: Request):
    return templates.TemplateResponse("RemoveBook.htm", context={"request": request, "remove_book_msg": ""})


@webapp.post("/RemovingBook", response_class=HTMLResponse)
def removing_book(request: Request, book_id=Form(...)):

    with open("Books.json", "r") as js_file:
        books = json.load(js_file)

    for i in range(len(books)):
        if int(book_id) == books[i]['id']:

            book_name = books[i]["title"]
            books.pop(i)
            with open("Books.json", "w") as js_file:
                json.dump(books, js_file)
            return templates.TemplateResponse("RemoveBook.htm", context={"request": request, "remove_book_msg": f"{book_name} removed"})
            break
        elif(i == len(books)-1):
            return templates.TemplateResponse("RemoveBook.htm", context={"request": request, "remove_book_msg": "Book not found"})

# *******************************************************
# ***********************Add Book************************


@webapp.get("/add book", response_class=HTMLResponse)
def add_book(request: Request):
    return templates.TemplateResponse("AddBook.htm", context={"request": request, "add_book_msg": ""})


@webapp.post("/AddingBook", response_class=HTMLResponse)
def saving_book_info(request: Request, add_book_author=Form(...), add_book_country=Form(...), add_book_pages=Form(...), add_book_name=Form(...), add_book_year=Form(...), books_id=Form(...)):

    adding_book_dict = {
        "id": int(books_id),
        "author": add_book_author.lower(),
        "country": add_book_country.lower(),
        "pages": int(add_book_pages),
        "title": add_book_name.lower(),
        "year": int(add_book_year)
    }
    with open("Books.json", "r") as js_file:
        BookList = json.load(js_file)

    for i in range(len(BookList)):
        if(adding_book_dict["id"] == BookList[i]["id"]):
            return templates.TemplateResponse("AddBook.htm", context={"request": request, "add_book_msg": "there is a same book in library"})
            break
        elif(i == len(BookList)-1):
            BookList.append(adding_book_dict)
            with open("Books.json", "w") as js_file:
                json.dump(BookList, js_file)
            return templates.TemplateResponse("AddBook.htm", context={"request": request, "add_book_msg": "book added successfully"})
