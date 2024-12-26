from fastapi import FastAPI
import models
from routers import user, posts, auth, comments, follows, likes, profiles
from database import engine

app = FastAPI()
app = FastAPI(
    title="Social-Media-Posts-and-Comments-using-FastAPI",
    description="API for managing User Registration and Posts ",
    version="1"
)
models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(follows.router)
app.include_router(likes.router)
app.include_router(profiles.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
