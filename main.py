import cv2
import reflection_detection as rd
import edge_detection as ed

from sys import argv
from sys import exit as sysexit

if len(argv) == 1:
    print("Usage: python main.py <image path>")
    sysexit()

img = cv2.imread(argv[1])
resized_img = cv2.resize(img, (320, 240))

#May differ depending on image brightness
reflections_img, reflections_perc = rd.process_image(resized_img, 180)
print("Reflections percentage: " + str(reflections_perc))
edges_image, line_amount = ed.detect_glasses(resized_img)
ed.sobel_detection(resized_img)

print("Line amount: " + str(line_amount))

cv2.imshow("Reflections", reflections_img)
cv2.imshow("Edges", edges_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
