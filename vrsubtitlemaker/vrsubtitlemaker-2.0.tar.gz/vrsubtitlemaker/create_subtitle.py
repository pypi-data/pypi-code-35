import kivy
kivy.require("1.0.9")

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.factory import Factory
from kivy.uix.popup import Popup

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

from vrsubtitlemaker.create_subtitle_lib import create_subtitle_lib

class SaveDialog(FloatLayout):
  save = ObjectProperty(None)
  text_input = ObjectProperty(None)
  cancel = ObjectProperty(None)

class CreateSubtitle(BoxLayout):

  def __init__(self, **kwargs):
    super(CreateSubtitle, self).__init__(**kwargs)
    self.mpl_f = plt.figure()
    self.mpl_a = self.mpl_f.add_subplot(111)
    self.preview_canvas = FigureCanvasKivyAgg(figure=self.mpl_f)
    self.ids.preview_container.add_widget(self.preview_canvas)

    self.text_piece_creator = create_subtitle_lib.TextPieceCreator()

    self.GeneratePreview()

  def GeneratePreview(self):
    font_color = [int(x * 255) for x in self.ids.font_color.color]
    bg_color = [int(x * 255) for x in self.ids.bg_color.color]
    text_piece = self.text_piece_creator.Create(
      text="Preview" if len(self.ids.text.text)==0 else self.ids.text.text,
      font_size=int(self.ids.font_size_input.text),
      padding=int(self.ids.padding_input.text),
      font_color=font_color,
      bg_color=bg_color,
      add_fading_border=self.ids.smooth_border_chkbox.active)

    self.mpl_a.clear()
    self.mpl_a.imshow(text_piece)
    self.preview_canvas.draw()
    return text_piece
    
  def DynamicPreview(self):
    if self.ids.dynamic_preview_chkbox.active:
      self.GeneratePreview()

  def Save(self):
    content = SaveDialog(save=self.save_img, cancel=self.dismiss_popup)
    self._popup = Popup(title="Save file", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def dismiss_popup(self):
    self._popup.dismiss()

  def save_img(self, path, filename):
    try:
      cv2.imwrite(os.path.join(path, filename),
                  cv2.cvtColor(self.GeneratePreview(), cv2.COLOR_RGBA2BGRA))
    except:
      print("ERROR: cannot save to", os.path.join(path, filename))
    self.dismiss_popup()

class CreateSubtitleApp(App):
  def build(self):
    Window.size = (1500, 600)
    return CreateSubtitle()


Factory.register('CreateSubtitle', cls=CreateSubtitle)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == "__main__":
  CreateSubtitleApp().run()