from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import math
import io
from PIL import Image

from .replace_color import ReplaceColorCython

def CropWhiteBorder(image):
  h, w, _ = image.shape
  
  mask = image[:,:,0] < 100

  coords = np.argwhere(mask)

  x0, y0 = coords.min(axis=0)
  x1, y1 = coords.max(axis=0)

  return image[x0:x1, y0:y1, :]

def AddBorder(image, padding, bg_color):
  h, w, c = image.shape
  image_padded = np.zeros((h + 2 * padding,w + 2 * padding,c), image.dtype)
  
  image_padded[:,:,:] = bg_color
  image_padded[padding:-padding, padding:-padding, :] = image
  
  return image_padded

def AddFadingBorder(image, padding, bg_color):
  h, w, c = image.shape
  image_padded = np.zeros((h + 2 * padding,w + 2 * padding,c), image.dtype)
  
  image_padded[:,:,:] = bg_color
  image_padded[padding:-padding, padding:-padding, :] = image
  
  for i in range(padding):
    for j in range(w + 2*padding):
      image_padded[i, j, 3] *= 1.0 * i / padding
      image_padded[-i, j, 3] *= 1.0 * i / padding
  return image_padded

class TextPieceCreator(object):
  def __init__(self):
    self.fig, self.ax = plt.subplots()
    self.ax.axis("off")
    self.text_prev = None
    
  def Create(self, text, font_size=10, padding=100,
             font_color=(0,0,0,255), bg_color=(255,255,120,255),
             add_fading_border=True):
    if self.text_prev != None:
      self.text_prev.remove()
    
    self.text_prev = self.fig.text(x=0, y=0.3, s=text,
                                   color=(0,0,0), fontsize=font_size)
    
    buf = io.BytesIO()
    self.fig.savefig(buf, format="tif", bbox_inches='tight', dpi=200)
    buf.seek(0)
    image = np.array(Image.open(buf))
    buf.close()

    image = CropWhiteBorder(image)
    ReplaceColorCython(image, font_color=np.array(font_color, np.uint8), bg_color=np.array(bg_color, np.uint8))
    image = AddBorder(image, padding, bg_color)
    if add_fading_border:
      image = AddFadingBorder(image, image.shape[0] // 20, bg_color)
    return image