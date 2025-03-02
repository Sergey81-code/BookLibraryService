from fastapi import FastAPI
import uvicorn

from api.core.config import get_settings
from api.routers import router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

@app.get('/')
async def ping():
    return {"Success": True}

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run("main:app", host="127.0.0.1", port=settings.APP_PORT, reload=True)
