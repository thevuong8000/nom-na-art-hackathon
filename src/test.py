import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2

img = np.zeros((400,600,3),np.uint8)
b,g,r,a = 0,255,0,0
cv2.imshow("res", img);
cv2.waitKey(0);
	
cv2.destroyAllWindows()
	#cv2.imwrite("res.png", img)