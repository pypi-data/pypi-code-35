import cv2


def defaultCam(imageName):
    imageName = "hi"
    cam = cv2.VideoCapture(0)
    ret, cap = cam.read()
    cv2.imwrite(imageName + ".jpg", cap)
    cam.release()
