# NOTE: the entry point for the api is the main.py file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import post, user, auth, like, comment
from . import config


# NOTE: not needed since there is alembic(database migration)
# models.Base.metadata.create_all(bind=database.engine)  # to create the tables


# create the app
app = FastAPI()


# allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# NOTE: The order of the routers matters.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)
app.include_router(comment.router)


@app.get("/")
def root():
    return {"message": "Welcome To Our NFT-Hub Folks!!"}
