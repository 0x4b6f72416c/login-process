import email
from fastapi import Depends, FastAPI, Request, status, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .schemas import User
from . import models
from .database import engine, SessionLocal
from app import schemas


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(engine)



@app.get('/', status_code=status.HTTP_200_OK ,response_class=HTMLResponse, tags=['login'])
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post('/login')
def process_login(username: str = Form(...), password: str = Form(...)):
    return {"username":username, "password":password}

@app.post('/create', status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_database)):
    new_user = models.User(email = request.username, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user