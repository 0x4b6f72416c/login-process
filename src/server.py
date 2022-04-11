from fastapi import FastAPI
from fastapi.responses import Response
import uvicorn


app = FastAPI()


@app.get('/')
def main_page():
    return Response("hello world")


if __name__ == "__main__":
    uvicorn.run(app)
