import uvicorn
from fastapi import FastAPI
import service.ocr as ocr_service
import time
import asyncio

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/ocr/{file_path}")
def read_item(file_path: str):
    res = ocr_service.read_image(file_path)
    return str(res)


# todo: pydantic 으로 인자 받을 수 있는 클래스 만들어야
@app.post("/ocr")
def read_item_post(file_path: str):
    res = ocr_service.read_image(file_path)
    return str(res)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)