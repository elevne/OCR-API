import time

import easyocr
import asyncio


reader = easyocr.Reader(['ko', 'en'], gpu=True)


# todo 1: 비동기처리 어떻게 해야하는지 알아보기 (알아낼 수 있을까...)
# todo 2: 이미지 URL 받아서 해당 주소의 이미지에 대한 처리하는 것으로 변경
def read_image(file_path: str):
    print("Start: "+str(time.time()))
    loop = asyncio.get_event_loop()
    res = reader.readtext(file_path, detail=0)
    print("End: "+str(time.time()))
    return res


print(read_image("./input.jpg"))
print(read_image("./output.jpg"))