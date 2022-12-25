# coding=utf8
import os
import cv2
from paddleocr import PPStructure, save_structure_res
import matplotlib.pyplot as plt
import pytesseract
import numpy as np

table_engine = PPStructure(table=True, layout=True, show_log=True, ocr=False)

save_folder = 'output'
img_path = 'img/6.jpg'
img = cv2.imread(img_path)
result = table_engine(img)

contours = np.array(result[2]["res"]["cell_bbox"])
contours = contours.astype(int).reshape((-1, 4, 2))

cells_txt = []
for contour in contours:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    cell_img = result[2]["img"][y: y+h, x: x+w]
    cell_txt = pytesseract.image_to_string(result[2]["img"][y: y+h, x: x+w], config = '--psm 6 -c tessedit_char_blacklist= ‘][|\/`', lang='rus')
    cell_txt = cell_txt.strip()
    cells_txt.append(cell_txt)

body = result[2]["res"]["html"][30:-30]
c = 0
trs = body.split("<tr>")
for i in range(len(trs)):
    trs[i] = trs[i][:-10].split("</td>")
    for j in range(len(trs[i])):
        trs[i][j] = trs[i][j].split(">")
        trs[i][j][0] += ">"
        trs[i][j][1] = cells_txt[c]
        c+=1

res = "<html><body><table><tbody>"
for tr in trs:
    res += "<tr>"
    for td in tr:
        res += td[0]
        res += td[1]
        res += "</td>"
    res += "</tr>"
res += "</tbody></table></body></html>"
print(res)