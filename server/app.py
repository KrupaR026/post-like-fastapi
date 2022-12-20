from fastapi import FastAPI
from server.routes.user import userRouter
from server.routes.post import postRouter
from server.routes.like import likeRouter


app = FastAPI()


@app.get("/")
def home():
    """simple home page routes

    Returns:
        _type_: _description_
    """
    return {"data": "you are at the home page"}


app.include_router(userRouter, tags=["User"])
app.include_router(postRouter, tags=["Post"])
app.include_router(likeRouter, tags=["Like"])