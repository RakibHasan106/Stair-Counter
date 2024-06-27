import numpy as np
import math
import cv2


# from matplotlib import pyplot as plt

class EdgeDetection:
    def __init__(self, img, sigma, kernelSize) -> None:
        self.img = img
        self.sigma = sigma
        self.kernelSize = kernelSize

    def gaussian_kernel(self):
        """returns a gaussian blur kernel"""
        sigma_x = self.sigma

        kernel = np.zeros((self.kernelSize, self.kernelSize))

        h = 1 / (2.0 * np.pi * sigma_x * sigma_x)

        n = self.kernelSize // 2

        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                p = ((i ** 2) + (j ** 2)) / (2 * (sigma_x ** 2))
                kernel[i + n, j + n] = h * np.exp(-p)

        print(kernel / np.min(kernel))
        return kernel

    def convolution(self, img, kernel):
        n = kernel.shape[0] // 2

        #img_bordered = cv2.copyMakeBorder(img, top=n , bottom=n , left=n , right=n, borderType=cv2.BORDER_CONSTANT)

        out = np.zeros((img.shape[0], self.img.shape[1], 1))

        for x in range(n, img.shape[0] - n):
            for y in range(n, img.shape[1] - n):
                sum = 0
                for i in range(-n, n + 1):
                    for j in range(-n, n + 1):
                        sum += img[x - i, y - j] * kernel[i + n, j + n]
                out[x, y] = sum

        return out

    def x_derivatives(self):
        kernel = np.zeros((self.kernelSize, self.kernelSize))

        n = self.kernelSize // 2

        h = 1 / (2.0 * math.pi * (self.sigma ** 2))

        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                p = ((i ** 2) + (j ** 2)) / (2 * (self.sigma ** 2))
                kernel[i + n, j + n] = (-i / (self.sigma ** 2)) * h * np.exp(-p)

        #print(kernel)
        return kernel

    def y_derivatives(self):
        kernel = np.zeros((self.kernelSize, self.kernelSize))
        n = self.kernelSize // 2

        h = 1 / (2.0 * math.pi * (self.sigma ** 2))

        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                p = ((i ** 2) + (j ** 2)) / (2 * (self.sigma ** 2))
                kernel[i + n, j + n] = (-j / (self.sigma ** 2)) * h * np.exp(-p)

        #print(kernel)
        return kernel

    def gradient_magnitude(self, img1, img2):
        m, n = img1.shape[0], img2.shape[1]
        output = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                output[i, j] = math.sqrt((img1[i, j] ** 2) + (img2[i, j] ** 2))

        return output

    def non_max_suppression(self, img, angle):

        m, n = img.shape[0], img.shape[1]
        out = np.zeros(img.shape)
        img = img / img.max() * 255

        for i in range(m - 1):
            for j in range(n - 1):
                try:
                    if 0 <= angle[i, j] < 22.5 or 157.5 <= angle[i, j] <= 180:
                        q = img[i, j + 1]
                        r = img[i, j - 1]
                    elif 22.5 <= angle[i, j] <= 67.5:
                        q = img[i - 1, j - 1]
                        r = img[i + 1, j + 1]
                    elif 67.5 <= angle[i, j] <= 112.5:
                        q = img[i - 1, j]
                        r = img[i + 1, j]
                    else:
                        q = img[i - 1, j + 1]
                        r = img[i + 1, j - 1]

                    if img[i, j] < q or img[i, j] < r:
                        out[i, j] = 0
                    else:
                        out[i, j] = img[i, j]

                except IndexError as e:
                    pass

        return out

    def find_threshold(self,img):

        oldThreshold = np.mean(img)

        newThreshold = self.threshold_generator(img, oldThreshold)

        while abs(newThreshold - oldThreshold) > 0.1 ** 6:
            oldThreshold = newThreshold
            newThreshold = self.threshold_generator(img, oldThreshold)

        return newThreshold

    def threshold_generator(self,img, threshold):
        m, n = img.shape

        sum1 = 0
        sum2 = 0
        n1 = 0
        n2 = 0

        for x in range(m):
            for y in range(n):
                if img[x, y] > threshold:
                    sum1 += img[x, y]
                    n1 += 1
                else:
                    sum2 += img[x, y]
                    n2 += 1

        highthreshold = sum1 / n1
        lowthreshold = sum2 / n2

        return (highthreshold + lowthreshold) / 2

    def doubleThresholding(self,img):

        threshold = self.find_threshold(img)

        weak = np.uint8(75)
        strong = np.uint8(255)

        out = np.zeros(img.shape)

        highThreshold = threshold * .5
        lowThreshold = highThreshold * .5

        strong_i, strong_j = np.where(img >= highThreshold)
        zeros_i, zeros_j = np.where(img <= lowThreshold)

        weak_i, weak_j = np.where((img >= lowThreshold) & (img <= highThreshold))

        out[strong_i, strong_j] = strong
        out[weak_i, weak_j] = weak
        out[zeros_i, zeros_j] = 0

        return out

    def hysteresis(self,img):

        out = img.copy()

        weak = 75
        strong = 255

        m, n = img.shape[0], img.shape[1]

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if out[i, j] == weak:
                    out[i, j] = strong if (
                                out[i - 1, j - 1] == strong or out[i - 1, j] == strong or out[i - 1, j + 1] == strong or
                                out[i, j - 1] == strong or out[i, j + 1] == strong or out[i + 1, j - 1] == strong or
                                out[i + 1, j] == strong or out[i + 1, j + 1] == strong) else 0

        return out

    def CannyEdgeDetector(self):
        blurred_img = self.convolution(self.img, self.gaussian_kernel())

        I_x = self.convolution(blurred_img, self.x_derivatives())
        I_y = self.convolution(blurred_img, self.y_derivatives())

        I_mag = self.gradient_magnitude(I_x, I_y)

        angles = np.arctan2(I_y.copy(), I_x.copy())

        nms = self.non_max_suppression(I_mag, angles)

        dbl_thresholded = self.doubleThresholding(nms)

        final_output = self.hysteresis(dbl_thresholded)

        cv2.normalize(final_output, final_output, 0, 255, cv2.NORM_MINMAX)
        final_output = np.round(final_output).astype(np.uint8)

        return final_output
