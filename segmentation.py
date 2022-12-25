# coding=utf8
import os
import base64
import cv2
from paddleocr import PPStructure
import matplotlib.pyplot as plt
import pytesseract

PATH_TO_TESSERACT = r"D:\Utilits\Tesseract-OCR\tesseract.exe"

def startSegmentation():
    pytesseract.pytesseract.tesseract_cmd = PATH_TO_TESSERACT
    plt.rcParams['figure.figsize'] = (15, 20)

def getSegmentation(filename):
    startSegmentation()
    table_engine = PPStructure(table=True, layout=True, show_log=True, ocr=False)
    img = cv2.imread(f'docs/{filename}')
    result = table_engine(img)
    txt_array = []
    for res in result:
        x1, y1, x2, y2 = res['bbox']
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img, res['type'], (x1, y1-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        #if res['type'] in ['text', 'reference']:
        txt_array.append(
            pytesseract.image_to_string(result[0]["img"], config='--psm 6 -c tessedit_char_blacklist= ‘][|\/`',
                                            lang='rus'))

    img_data = cv2.imencode('.png', img)[1].tostring()
    img_data = base64.b64encode(img_data)
    img_data = img_data.decode()
    return img_data, txt_array

