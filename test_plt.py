# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_plt.py 
   Description :   None
   Author :        LSQ
   date：          2020/8/30
-------------------------------------------------
   Change Activity:
                   2020/8/30: None
-------------------------------------------------
"""
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import pytesseract
import requests
from fake_useragent import UserAgent

# x_list = [[142, 143, 184, 215, 307, 368, 408, 422, 428, 432, 435, 435, 435, 435, 428, 409, 352, 315, 250, 163, 105, 43, 43, 108, 173, 273, 343, 463, 504, 524, 524, 511, 494, 464, 343, 261, 175, 122, 67, 56], [425, 425, 376, 341, 284, 223, 169, 135, 135, 135, 177, 220, 273, 344, 425]]
# y_list = [[151, 89, 62, 35, 35, 73, 137, 191, 217, 245, 262, 300, 314, 313, 319, 281, 249, 223, 223, 223, 288, 354, 570, 641, 710, 710, 710, 633, 562, 484, 356, 214, 131, 49, -39, -39, -39, 0, 57, 144], [466, 544, 590, 635, 635, 648, 586, 539, 459, 387, 345, 301, 301, 301, 391]]

# x_list = [420, 403, 386, 349, 296, 256, 220, 177, 155, 142, 128, 128, 161, 254, 315, 395, 459, 528, 522, 522, 463, 360,
#           293, 180, 110, 36, 39, 39, 117, 185, 294, 388, 443, 498, 510, 431, 142, 142, 182, 253, 292, 347, 430, 430,
#           430, 349, 228, 194, 142]
# y_list = [521, 574, 597, 635, 635, 635, 621, 580, 522, 492, 407, 352, 402, 449, 452, 449, 382, 316, 211, 143, 24, -39,
#           -48, -39, 43, 124, 317, 530, 616, 710, 721, 710, 663, 614, 537, 521, 211, 166, 79, 35, 35, 35, 127, 209, 281,
#           370, 370, 316, 282]


x_list = [[319, 331, 13, 11],[347, 421, 421, 520, 520, 417, 421, 322, 331, 332, 101, 323]]
y_list = [[-26, 135, 138, 219],[693, 717, 229, 241, 162, 151, -20, -22, 236, 564, 232, 217]]
x_list_2 = [319, 331, 13, 11,347, 421, 421, 520, 520, 417, 421, 322, 331, 332, 101, 323]
y_list_2 = [-26, 135, 138, 219,693, 717, 229, 241, 162, 151, -20, -22, 236, 564, 232, 217]
# for i in zip(x_list, y_list):
#     print(i)
# xy_list = [(x, y) for x, y in zip(x_list, y_list)]
# list_a = []
# list_b = []
# for index, coordinate in enumerate(xy_list[:-1], start=1):
#     if abs(xy_list[index][0] - coordinate[0]) > 150 and abs(xy_list[index][1] - coordinate[1]) > 150:
#         list_a = xy_list[:index]
#         list_b = xy_list[index:]
#         # break
# print(list_a)
# print(list_b)
# tuple_list = [(x,y) for x,y in zip(x_list_2,y_list_2)]
# print(tuple_list)
# plt.figure(figsize=(1, 1))
# plt.fill(x_list[0],y_list[0], x_list[1], y_list[1])
# plt.plot(x_list_2,y_list_2)
# plt.axis('off')
# bio = BytesIO()
# plt.savefig(bio)
# plt.show()
# im = Image.open(bio)
# print(pytesseract.image_to_string(im, config='--psm 10')[0])

# headers = {'User-Agent': UserAgent().random}
# resp = requests.get('https:' + '//vip.gxrc.com/Public/Phone/0F555FA2-D465-435E-9A94-1FACA77FD9C0', headers=headers)
# bio = BytesIO(resp.content)
# im = Image.open(bio)
# print(pytesseract.image_to_string(im))
