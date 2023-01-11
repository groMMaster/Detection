# coding=utf8
import os
import base64
import cv2
from paddleocr import PPStructure
import matplotlib.pyplot as plt
import pytesseract
import numpy as np

PATH_TO_TESSERACT = r"D:\Utilits\Tesseract-OCR\tesseract.exe"


def startSegmentation():
    pytesseract.pytesseract.tesseract_cmd = PATH_TO_TESSERACT
    plt.rcParams['figure.figsize'] = (15, 20)


def getSegmentation(filename):
    startSegmentation()
    table_engine = PPStructure(table=True, layout=True, show_log=True, ocr=False)
    img = cv2.imread(f'docs/{filename}')
    img_post = img.copy()

    result = table_engine(img)
    txt_array = []
    table_array = []
    for res in result:
        x1, y1, x2, y2 = res['bbox']
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img, res['type'], (x1, y1-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.rectangle(img_post, (x1, y1), (x2, y2), (255, 255, 255), -1)

        if res["type"] == "text" or res["type"] == "title":
            txt_array.append(
                pytesseract.image_to_string(res["img"], config='--psm 6 -c tessedit_char_blacklist= ‘][|\/`', lang='rus'))
        if res["type"] == "table":
            table_array.append(GetHtmlTable(res))

    txt_array.append(
        pytesseract.image_to_string(img_post, config='--psm 6 -c tessedit_char_blacklist= ‘][|\/`', lang='rus'))

    img_data = cv2.imencode('.png', img)[1].tostring()
    img_data = base64.b64encode(img_data)
    img_data = img_data.decode()
    return img_data, txt_array, table_array


def GetHtmlTable(table):
    contours = np.array(table["res"]["cell_bbox"])
    contours = contours.astype(int).reshape((-1, 4, 2))

    cells_txt = []
    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        cell_img = table["img"][y: y + h, x: x + w]
        cell_txt = pytesseract.image_to_string(table["img"][y: y + h, x: x + w],
                                               config='--psm 6 -c tessedit_char_blacklist= ‘][|\/`', lang='rus')
        cell_txt = cell_txt.strip()
        cells_txt.append(cell_txt)

    body = table["res"]["html"][30:-30]
    c = 0
    trs = body.split("<tr>")
    for i in range(len(trs)):
        trs[i] = trs[i][:-10].split("</td>")
        for j in range(len(trs[i])):
            trs[i][j] = trs[i][j].split(">")
            trs[i][j][0] += ">"
            try:
                trs[i][j][1] = cells_txt[c]
            except IndexError:
                trs[i][j].append("")
            c += 1

    res = "<table><tbody>"
    for tr in trs:
        res += "<tr>"
        for td in tr:
            res += td[0]
            res += td[1]
            res += "</td>"
        res += "</tr>"
    res += "</tbody></table>"
    return res
