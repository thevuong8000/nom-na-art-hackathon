import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import time
import random
import json
from googletrans import Translator
translator = Translator()

with open("../data/nom.json") as file:
	data = json.load(file)

def getWord(arr):
	## Make canvas and set the color
	img = np.zeros((400,600,3),np.uint8)
	b,g,r,a = 0,255,0,0
	fontpath = "./simsun.ttc" # <== 这里是宋体路径 
	font = ImageFont.truetype(fontpath, 32)
	img_pil = Image.fromarray(img)
	draw = ImageDraw.Draw(img_pil)
	x, y = 50, 50
	for word in arr:
		endword = translator.translate(word['mean'], dest='en').text
		draw.text((x, y), word['text'] + " in English means " + '"' + endword + '"', font = font, fill = (b, g, r, a))
		y += 30
	img = np.array(img_pil)
	## Display 
	cv2.imwrite("res.png", img);
	if cv2.waitKey(1) == ord('q'):
		cv2.destroyAllWindows()
	
def getQuestion(knowledge):
	ans = random.choice(knowledge)
	arr = [ans['mean']]
	img = np.zeros((400,600,3),np.uint8)
	b,g,r,a = 0,255,0,0
	fontpath = "./simsun.ttc" # <== 这里是宋体路径 
	font = ImageFont.truetype(fontpath, 32)
	img_pil = Image.fromarray(img)
	draw = ImageDraw.Draw(img_pil)
	x, y = 50, 50
	arr.append(random.choice(data)['mean'])
	arr.append(random.choice(data)['mean'])
	arr.append(random.choice(data)['mean'])
	draw.text((50, 50), "What does " + ans['text'] + " mean in English?", font = font, fill = (b, g, r, a))
	for i in range(len(arr)):
		arr[i] = translator.translate(arr[i], dest='en').text
	draw.text((50, 100), "A. " + arr[0], font = font, fill = (b, g, r, a))
	draw.text((50, 150), "B. " + arr[1], font = font, fill = (b, g, r, a))
	draw.text((50, 200), "C. " + arr[2], font = font, fill = (b, g, r, a))
	draw.text((50, 250), "D. " + arr[3], font = font, fill = (b, g, r, a))
	img = np.array(img_pil)
	## Display 
	cv2.imwrite("ques.png", img);
	# if cv2.waitKey(1) == ord('q'):
		# cv2.destroyAllWindows()

cv2.destroyAllWindows()
	#cv2.imwrite("res.png", img)