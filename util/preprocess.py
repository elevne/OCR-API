import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
import requests
from imutils.perspective import four_point_transform


def plt_imshow(title='Image', img=None, figsize=(8, 5)):
    if len(img.shape) < 3:
        rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgbImg)
    plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.show()


def outline(image, width, ksize=(5, 5), min_threshold=75, max_threshold=200):
    image2 = imutils.resize(image, width=width)
    ratio = image.shape[1] / float(image2.shape[1])

    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, ksize, 0)
    edged = cv2.Canny(blurred, min_threshold, max_threshold)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    findCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            findCnt = approx
            break

    if findCnt is None:
        raise Exception(("Could not find outline."))

    output = image2.copy()
    cv2.drawContours(output, [findCnt], -1, (0, 255, 0), 2)
    transform_image = four_point_transform(image, findCnt.reshape(4, 2) * ratio)
    plt_imshow("Transform", transform_image)
    return transform_image


url = 'https://ww.namu.la/s/8a637fc771fcff0b619992ca54499777f6a7e73a6dd4e1b816b7ef32e7473b48cc19c72ae3a3073cd7f3f24451f0b8a6193f460ba8f41f42dd913e82f8e7612a80a062d2e0a6406a82b0d03e2823ee56d9b0b190d73c3ca5228322b88baf7b1b'
image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
business_card_image = outline(org_image, width=200, ksize=(5, 5), min_threshold=20, max_threshold=100)