import cv2
import numpy as np

# Load the image
image_path = 'stairs 2.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img, None, fx=0.2, fy=0.2)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection (if needed)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Run HoughLinesP
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# Draw detected lines on the original image (optional)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the image with detected lines (optional)
cv2.imshow('Image with Hough Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the number of detected lines
if lines is not None:
    print(f"Number of lines detected: {len(lines)}")
else:
    print("No lines detected.")

