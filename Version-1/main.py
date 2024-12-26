from fastapi import FastAPI
import models
from routers import user, posts
from database import engine

app = FastAPI()
app = FastAPI(
    title="Social-Media-Posti-using-FastAPI",
    description="API for managing User Registration and Posts ",
    version="1"
)
models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(posts.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
