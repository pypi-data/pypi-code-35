from subprocess import call

from cv2 import VideoCapture


def safe_format(x):
    if x is None:
        return 0
    return x


class CameraManager:
    def __init__(self, width, height, port=0):
        self.port = port
        self.width = width
        self.height = height
        self.camera = self.initialize_camera(port, self.width, self.height)

    def initialize_camera(self, port, width, height):
        camera = VideoCapture(port)
        camera.set(3, width)
        camera.set(4, height)
        return camera

    def set_camera(self, port):
        if self.port is not port:
            try:
                port = int(port)
                self.camera.release()
                self.camera = self.initialize_camera(port, self.width, self.height)
                self.port = port
            except ValueError as e:
                pass

    def set_exposure(self, exposure):
        call(['v4l2-ctl', '--device=/dev/video{}'.format(safe_format(self.port)), '-c',
              'exposure_auto=1', '-c', 'exposure_absolute={}'.format(safe_format(exposure))])

    def get_image(self):
        success, img = self.camera.read()
        if success:
            return img

    def release(self):
        self.camera.release()
