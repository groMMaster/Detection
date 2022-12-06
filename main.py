import os
import cv2
from paddleocr import PPStructure
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

plt.rcParams['figure.figsize'] = (15, 20)

table_engine = PPStructure(table=False, ocr=False, show_log=True)

img_path = 'img/2.jpeg'
img = cv2.imread(img_path)
print(img.shape)
result = table_engine(img)


for res in result:
    x1, y1, x2, y2 = res['bbox']
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(img, res['type'], (x1, y1-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if res['type'] in ['text', 'reference']:
      print(pytesseract.image_to_string(img[y1:y1+y2-y1, x1:x1+x2-x1], config='--psm 6', lang='rus'))
      print("--------------------------------------------------------------------------------------------------")

plt.imshow(img)
plt.show()