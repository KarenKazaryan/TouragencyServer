import fastapi
import uvicorn
from fastapi import FastAPI

from src.database.database import Base, engine
from src.server.routers.router import routers

app = FastAPI()

[app.include_router(router) for router in routers]


@app.get("/", tags=['Docs'])
def docs():
    return fastapi.responses.RedirectResponse(url="/docs")


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8099, reload=True)
