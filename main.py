from fastapi import FastAPI
import service.ocr as ocr_service

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/ocr/{file_path}")
async def read_item(file_path: str):
    return str(ocr_service.read_image(file_path))


# todo: pydantic 으로 인자 받을 수 있는 클래스 만들어야
@app.post("/ocr")
async def read_item_post(file_path: str):
    return str(ocr_service.read_image(file_path))
