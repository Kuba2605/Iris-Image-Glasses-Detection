import cv2
import numpy as np
from math import pi

def sobel_detection(input_image):
    grayscale = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(grayscale, (3,3), 0)
    
    #sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobely = cv2.GaussianBlur(sobely, (3,3), 0)
    sobely = (255 - sobely)
    sobely = cv2.morphologyEx(sobely, cv2.MORPH_RECT, np.ones((5,5), np.uint8))
    
    
    #cv2.imshow('Sobel Y', sobely)
    
def detect_glasses(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 100)
    
    
    # Define region of interest (ROI) as the ocular area
    rows, cols = edges.shape[:2]
    mask = np.zeros_like(edges)
    bottom_left = [0, rows]
    bottom_right = [cols, rows]
    top_left = [0, 0]
    top_right = [cols, 0]
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, 255)
    edges = cv2.bitwise_and(edges, mask)
    
    # Define kernel for dilation
    kernel = np.ones((5,5),np.uint8)
    edges = cv2.dilate(edges,kernel,iterations = 1)
    #cv2.imshow('Canny', edges)
    
    # Define the Hough transform parameters
    rho = 1
    theta = np.pi/180
    threshold = 25
    min_line_length = 50
    max_line_gap = 2
    
    # Run Hough transform on the edges image
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    
    # Iterate over the lines and draw them on the original image
    line_amount = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            #if (y2-y1)/(x2-x1) < 0: # Checking the inclination of the lines
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_amount += 1
    return image, line_amount