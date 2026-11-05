import cv2

image = cv2.imread("test.png")


if image is None:
    raise FileNotFoundError("Could not load test.png")

print(image.dtype)

print (type(image))