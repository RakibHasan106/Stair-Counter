import cv2
import numpy as np

# Load the image
img = cv2.imread("stairs 2.jpg")
img = cv2.resize(img, None, fx=0.2, fy=0.2)
cv2.imshow("Source", img)

# Apply Gaussian blur to get good results
img_blur = cv2.GaussianBlur(img, (5, 5), 0)

# Edge detection using Canny
dst = cv2.Canny(img_blur, 80, 240, 3)
out_img = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
control = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

# Line detection using HoughLinesP
lines = cv2.HoughLinesP(dst, 1, np.pi / 180, 30, minLineLength=60, maxLineGap=5)



y_keeper_for_lines = []

if lines is not None:
    for i in range(1, len(lines)):
        l = lines[i][0]
        cv2.line(control, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

    l = lines[0][0]
    cv2.line(out_img, (0, l[1]), (img.shape[1], l[1]), (0, 0, 255), 3, cv2.LINE_AA)
    y_keeper_for_lines.append(l[1])

    okey = 1
    stair_counter = 1
    
    print(lines)

    for i in range(1, len(lines)):
        l = lines[i][0]
        for m in y_keeper_for_lines:
            if abs(m - l[1]) < 15:
                okey = 0

        if okey:
            cv2.line(out_img, (0, l[1]), (img.shape[1], l[1]), (0, 0, 255), 3, cv2.LINE_AA)
            y_keeper_for_lines.append(l[1])
            stair_counter += 1
        okey = 1

    cv2.putText(out_img, "Stair number:" + str(stair_counter), (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    cv2.imshow("Before", img)
    cv2.imshow("Control", control)
    cv2.imshow("Detected lines", out_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
