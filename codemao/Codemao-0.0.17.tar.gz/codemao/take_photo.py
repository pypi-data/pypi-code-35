import cv2
import sys
import os


def take_photo():
    classfier_xml_path = os.path.abspath(os.path.join(
        cv2.__file__,
        "../data/haarcascade_frontalface_alt.xml"
    ))
    classfier = cv2.CascadeClassifier(classfier_xml_path)
    if len(sys.argv) > 2:
        save_as = sys.argv[1]
        key = sys.argv[2]
    else:
        raise TypeError("No path or key found")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        try:
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            raise IOError("No camera on computer.")
            return
        # TODO:fix chinese in the xml load path
        try:
            faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 10, minSize = (32, 32))
        except cv2.error:
            raise TypeError("OpenCV not working properly due to Chinese in the load path")
            return
        cv2.imshow("img", frame)
        # Close window on SpaceBar pressed.
        if ((key == "f" and len(faceRects) > 0) or (cv2.waitKey(1) & 0xff) == ord(key)):
            cv2.imencode('.png',frame)[1].tofile(save_as)
            cv2.destroyAllWindows()
            break
    cap.release()

if __name__ == "__main__":
    take_photo()
