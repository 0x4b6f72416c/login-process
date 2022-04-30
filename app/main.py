
from curses.ascii import SI
from http.client import HTTPException
from urllib import request
from fastapi import Depends, FastAPI, Request, status, Form, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .schemas import User
from . import models
from .database import engine, SessionLocal
from app import schemas
from passlib.context import CryptContext
from .token import Sign
from app import token


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(engine)



@app.get('/', status_code=status.HTTP_200_OK ,response_class=HTMLResponse, tags=['login'])
def index_page(request: Request, username: str | None = Cookie(None), db: Session = Depends(get_database)):
    if not username:
        return templates.TemplateResponse("index.html", {"request":request}) 
    user = db.query(models.User).filter(models.User.email == Sign.get_username_from_sign(username)).first()
    if not user:
        return templates.TemplateResponse("index.html", {"request":request})
    valid_username = Sign.get_username_from_sign(username)
    if not valid_username:
        return templates.TemplateResponse("index.html", {"request":request}) 
    return templates.TemplateResponse('index_cookie.html',{"request":request, "username":user.email})

@app.post('/login',status_code=status.HTTP_202_ACCEPTED, tags=['authentication'])
def process_login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_database)):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid credentails")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Incorrect password")
    response = Response()
    username_sign = Sign.sign_username(username)
    response.set_cookie(key="username", value=username_sign)
    return response


@app.post('/create', status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_database)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(email = request.username, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user