
import win32clipboard
from cStringIO import StringIO
from PIL import ImageGrab as PilImageGrab


class WindowsBackend(BaseBackend):
    """ Windows clipboard backend

    This backends the windows clipboard via the win32clipboard module.
    This means that there is less code to write, because a fair amount
    of it is already written. This backend really just takes its functionality
    and makes it compatible with the frontend. Also, it uses the PIL.ImageGrab
    module to get images from the clipboard, so PIL.Image is considered the
    native image type
    """

    @staticmethod
    def get_native_image_str():
        return 'pil'

    @staticmethod
    def get_native_image_type():
        return PilImage

    def __init__(self):
        """ Constructs a new object

        There isn't really an internal clipboard object to manage. Instead, just
        open the clipboard
        """
        win32clipboard.OpenClipboard()

    def __del__(self):
        win32clipboard.CloseClipboard()

    def get_text(self):   
        """ Synchronously get text

        Preform a blocking call to get text from the clipboard

        Returns
        -------
        str or None
            String if text is ever gotten, or None if there is no text
        """
        return win32clipboard.GetClipboardData()

    def get_image(self, format='Pil'):
        """ Synchronously get image

        Preform a blocking call to get an image from the clipboard

        Params
        ----------
        format : str (optional)
            Format of the image. Default is 'Pil', which refers to
            PIL.Image, but implementation is left to each function

        Returns
        -------
        PIL.Image or None
            Image from clipboard, or None if not available
        """
        return PilImageGrab.grabclipboard()

    def set_text(self, text):
        """ Synchronously sets text

        Preform a blocking call to set text on the clipboard

        Params
        ----------
        text : str
            Text to add to clipboard
        """
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboard(text.encode('utf-8'), win32clipboard.CF_TEXT)

    def set_image(self, img, format='pil'):
        """ Synchronously sets image

        Preform a blocking call to set image on the clipboard

        Params
        ----------
        image : PIL.Image
            Image to add to clipboard
        """
        output = StringIO()
        img.convert("RGB").save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
