from fastapi import FastAPI
from api.books.handlers import book_router
import uvicorn

app = FastAPI(title="Book Library")

app.include_router(book_router, prefix="/books", tags=["books"])

@app.get('/')
async def ping():
    return {"Success": True}

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
