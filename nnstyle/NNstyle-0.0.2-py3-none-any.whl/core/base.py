class BaseImage(object):
    """
    Base Class
    """
    kind = None

    def __init__(self, width, depth, height, *args, **kwargs):
        self.width = width
        self.depth = depth
        self.height = height
        self.BGwidth, self.BGheight = self.image_size()
        self._img = self.new_image(**kwargs)

    def new_image(self, **kwargs):  # pragma: no cover
        """
        Build Image Class. SubClass should return the class created
        """
        return None

    def get_image(self, **kwargs):
        """
        Return the image class for further processing.
        """
        return self._img

    def save(self, stream, kind=None):
        """
        Save the image file.
        """
        raise NotImplementedError("BaseImage.save")

    def image_size(self):
        """
        Caculate Size.
        """
        raise NotImplementedError("BaseImage.save")
