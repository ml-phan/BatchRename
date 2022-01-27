import cv2 as cv
import numpy as np

events = [i for i in dir(cv) if "EVENT" in i]
print(events)

# mouse callback function
# def draw_circle(event, x, y, flags, param):
    


# create a black image
# img = np.zeros((512, 512, 3), np.uint8)):

# cv.line(img, (0, 0), (511, 511), (255, 0, 0), 2)
# cv.rectangle(img, (50, 50), (400, 400), (255, 255, 0), 1)
# cv.circle(img, (200, 210), 50, (0, 255, 0), 1)
# pts = np.array([[20, 20], [200, 20], [200, 200], [20, 200]], np.int32)
# pts2 = pts.reshape((-1, 1, 2))
# cv.polylines(img, [pts2], True, (0, 255, 255))
# cv.imshow("Example", img)

# img = cv.imread(cv.samples.findFile("src/range-rover.jpeg"), cv.IMREAD_GRAYSCALE)
#
# if img is None:
#     print("Could not fine image")
#
# cv.imshow("Display", img)
# k = cv.waitKey(0)
#
# if k == ord("s"):
#     cv.imwrite("src/range-rover.png", img)

# cap = cv.VideoCapture("src/test-vid.avi")
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     # if frame is read correctly, ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#
#     cv.imshow("frame", gray)
#     if cv.waitKey(1) == ord("q"):
#         break
#
# cap.release()
# cv.destroyAllWindows()

k = cv.waitKey(0)
