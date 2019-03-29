import kivy
kivy.require("1.0.9")

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.factory import Factory
from kivy.uix.popup import Popup

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import cv2
import glob

from vrsubtitlemaker.add_patterns_lib.wrap_pattern import WrapPattern
from vrsubtitlemaker.add_patterns_lib.alpha_blend import AlphaBlend


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
  ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
  ''' Add selection support to the Label '''
  index = None
  selected = BooleanProperty(False)
  selectable = BooleanProperty(True)

  def refresh_view_attrs(self, rv, index, data):
    ''' Catch and handle the view changes '''
    self.index = index
    return super(SelectableLabel, self).refresh_view_attrs(
        rv, index, data)

  def on_touch_down(self, touch):
    ''' Add selection on touch down '''
    if super(SelectableLabel, self).on_touch_down(touch):
      return True
    if self.collide_point(*touch.pos) and self.selectable:
      return self.parent.select_with_touch(self.index, touch)

  def apply_selection(self, rv, index, is_selected):
    ''' Respond to the selection of items in the view. '''
    self.selected = is_selected
    if is_selected:
      print("[Selection]: selection changed to {0}".format(rv.data[index]))
    else:
      print("[Selection]: selection removed for {0}".format(rv.data[index]))
    rv.Event()

class RV(RecycleView):
  def __init__(self, **kwargs):
    super(RV, self).__init__(**kwargs)
  def Event(self):    
    self.parent.parent.parent.parent.parent.parent.RecycleViewClick()

class LoadDialog(FloatLayout):
  load = ObjectProperty(None)
  cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
  save = ObjectProperty(None)
  text_input = ObjectProperty(None)
  cancel = ObjectProperty(None)

class Pattern(object):
  def __init__(self, filename, pattern, azimuth=None, elevation=None, depth=None, ppc=None):
    self.filename = filename
    self.pattern = pattern
    self.azimuth = azimuth
    self.elevation = elevation
    self.depth = depth
    self.ppc = ppc

class AddPatterns(BoxLayout):
  def __init__(self, **kwargs):
    super(AddPatterns, self).__init__(**kwargs)
    self.mpl_f_pattern_preview = plt.figure()
    self.mpl_a_pattern_preview = self.mpl_f_pattern_preview.add_subplot(111)
    self.pattern_preview_canvas = FigureCanvasKivyAgg(figure=self.mpl_f_pattern_preview)
    self.ids.pattern_preview_container.add_widget(self.pattern_preview_canvas)

    self.mpl_f_preview = plt.figure()
    self.mpl_a_preview = self.mpl_f_preview.add_subplot(111)
    self.preview_canvas = FigureCanvasKivyAgg(figure=self.mpl_f_preview)
    self.ids.preview_container.add_widget(self.preview_canvas)

    self.mpl_f_preview .canvas.mpl_connect('button_press_event', self.OnPreviewClick)

    self.vr_image = None
    self.image_blended = None
    self.patterns_on_the_list = []
    self.patterns_applied = []

    self.ipd = 0.05
    self.azimuth = self.ids.azimuth_slider.value
    self.elevation = self.ids.elevation_slider.value
    self.depth = self.ids.depth_slider.value
    self.ppc = self.ids.ppc_slider.value
    
    self.auxiliaries = []
    self.show_auxiliaries = True
    self.UpdatePreview()

  def UpdateStatus(self, msg):
    self.ids.status.text = msg

  def OnPreviewClick(self, event):
    if event.xdata is None or event.ydata is None:
      return

    px = float(event.xdata)
    py = float(event.ydata)
    img_width = self.vr_image.shape[1]
    img_height = self.vr_image.shape[1] // 2

    if px < 0 or py < 0 or px > img_width * 2 or py > img_height * 2:
      return
    
    self.elevation = -1.0 * (py % img_height - img_height // 2) / img_height * 180
    if py < img_height:
      self.azimuth = 1.0 * (px - img_width // 2) / img_width * 360
    else:
      r_azimuth = 1.0 * (px - img_width // 2) / img_width * 360
      self.azimuth = r_azimuth + (180 - 2 * math.degrees(math.atan(self.depth / self.ipd)))

    self.ids.azimuth_slider.value = int(self.azimuth)
    self.ids.elevation_slider.value = int(self.elevation)
    self.ids.azimuth_input.value = "%d" % self.azimuth
    self.ids.elevation_input.value = "%d" % self.elevation
    self.UpdateAuxiliary()
  
  def ToggleAuxiliary(self):
    self.show_auxiliaries = not self.show_auxiliaries
    self.UpdateAuxiliary()
  
  def UpdateAuxiliary(self):
    for aux in self.auxiliaries:
      try:
        aux.remove()
      except:
        pass
    self.auxiliaries = []

    if self.show_auxiliaries:
      l, = self.mpl_a_preview.plot([0, self.vr_image.shape[1]], [self.vr_image.shape[0]//2, self.vr_image.shape[0]//2], "w--")
      self.auxiliaries.append(l)

      l, = self.mpl_a_preview.plot([self.vr_image.shape[1] // 2, self.vr_image.shape[1] //2 ],
                                   [0, self.vr_image.shape[0]], "w--")
      self.auxiliaries.append(l)

      img_width = self.vr_image.shape[1]
      img_height = self.vr_image.shape[1] // 2
    
      lx = self.azimuth / 360 * img_width + img_width // 2
      r_azimuth = self.azimuth - (180 - 2 * math.degrees(math.atan(self.depth / self.ipd)))
      rx = r_azimuth / 360 * img_width + img_width // 2
      y = -self.elevation / 180 * img_height + img_height // 2

      dot, = self.mpl_a_preview.plot([lx % img_width], [y], 'o', color="red", markersize=5/self.ppc)
      self.auxiliaries.append(dot)
      dot, = self.mpl_a_preview.plot([rx % img_width], [y + img_height], 'o', color="red", markersize=5/self.ppc)
      self.auxiliaries.append(dot)
      self.mpl_a_preview.axis("on")

    else:
      self.mpl_a_preview.axis("off")

    self.preview_canvas.draw()

    # Update Pattern's parameters
    id_selected = self.ids.patterns_list.layout_manager.selected_nodes
    if len(id_selected) != 0:
      self.patterns_on_the_list[id_selected[0]].azimuth = self.azimuth
      self.patterns_on_the_list[id_selected[0]].elevation = self.elevation
      self.patterns_on_the_list[id_selected[0]].depth = self.depth
      self.patterns_on_the_list[id_selected[0]].ppc = self.ppc


  def UsePlainBackground(self):
    width = int(self.ids.width_input.text)
    height = int(self.ids.height_input.text)
    bg_color = self.ids.bg_color.color

    bg_img = np.zeros((height, width, 4), np.uint8)
    bg_color_255 = [int(x * 255) for x in bg_color]
    bg_img[:,:,:] = bg_color_255
    self.vr_image = bg_img

    self.UpdatePreview()

    print("[UsePlainBackground]: selected plain background (%d, %d) of color (%d, %d, %d, %d)" % (width, height, bg_color_255[0], bg_color_255[1], bg_color_255[2], bg_color_255[3]))
    self.UpdateStatus("[UsePlainBackground]: done.")


  def UpdatePreview(self):
    print("[UpdatePreview]: Begin")
    # self.UpdateStatus("[UpdatePreview]: Begin")
    if self.vr_image is None:
      self.UsePlainBackground()
    self.image_blended = np.array(self.vr_image)

    if len(self.patterns_applied) > 0:
      AlphaBlend(self.image_blended, self.patterns_applied[-1], self.image_blended)

    self.mpl_a_preview.clear()

    self.mpl_a_preview.imshow(self.image_blended)
    self.mpl_a_preview.set_ylim(self.vr_image.shape[0], 0)
    self.mpl_a_preview.set_xlim(0, self.vr_image.shape[1])

    self.preview_canvas.draw()

    self.UpdateAuxiliary()
    print("[UpdatePreview]: Done")
    # self.UpdateStatus("[UpdatePreview]: Done")

  def LoadVRImage(self):
    content = LoadDialog(load=self.load_vr_image, cancel=self.dismiss_popup)
    self._popup = Popup(title="Load VR image", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def load_vr_image(self, path, filename):
    # Implementation
    try:
      img = cv2.imread(filename[0], cv2.IMREAD_UNCHANGED)
      n_channels = img.shape[2]
      if n_channels == 1:
        self.vr_image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
      elif n_channels == 3:
        self.vr_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
      elif n_channels == 4:
        self.vr_image = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
      else:
        print("[LoadVrImage]: Error while loading:", filename[0], "(# of channels: %d)" % n_channels)
        self.UpdateStatus("[LoadVrImage]: error (2).")
      
    except:
      print("[LoadVrImage]: Error while loading:", filename)
      self.UpdateStatus("[LoadVrImage]: error (1).")
      return

    print("[LoadVrImage]: loaded", filename[0], "shape", self.vr_image.shape)
    self.UpdateStatus("[LoadVrImage]: done.")
    self.dismiss_popup()
    self.UpdatePreview()

    self.ids.width_input.text = str(self.vr_image.shape[1])
    self.ids.height_input.text = str(self.vr_image.shape[0])

  def AddNewPattern(self):
    content = LoadDialog(load=self.add_new_pattern, cancel=self.dismiss_popup)
    self._popup = Popup(title="Load a new pattern", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def add_new_pattern(self, path, filename):
    # Implementation
    try:
      img = cv2.imread(filename[0], cv2.IMREAD_UNCHANGED)
      n_channels = img.shape[2]
      if n_channels == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
      elif n_channels == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
      elif n_channels == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
      else:
        print("[AddNewPattern]: Error while loading:", filename[0], "(# of channels: %d)" % n_channels)
        self.UpdateStatus("[AddNewPattern]: error (2).")
    except:
      print("[AddNewPattern]: Error while loading:", filename)
      self.UpdateStatus("[AddNewPattern]: error(1).")
      return

    self.dismiss_popup()

    self.patterns_on_the_list.append(Pattern(filename[0], img, self.azimuth, self.elevation, self.depth, self.ppc))
    len_list = len(self.patterns_on_the_list)
    self.ids.patterns_list.layout_manager.selected_nodes = [len_list - 1]
    self.UpdatePatternList()

    print("[AddNewPattern]: done loading", filename[0])
    self.UpdateStatus("[AddNewPattern]: done.")

  def UpdatePatternList(self):
    self.ids.patterns_list.data = [{"text": os.path.basename(pattern.filename)} for pattern in self.patterns_on_the_list]

  def RemoveSelectedPattern(self):
    id_selected = self.ids.patterns_list.layout_manager.selected_nodes
    if len(id_selected) == 0:
      return
    self.patterns_on_the_list = self.patterns_on_the_list[:id_selected[0]] + self.patterns_on_the_list[id_selected[0] + 1:]
    self.UpdatePatternList()

  def RecycleViewClick(self):
    id_selected = self.ids.patterns_list.layout_manager.selected_nodes
    if len(id_selected) == 0:
      return

    pattern = self.patterns_on_the_list[id_selected[0]]
    
    # Update pattern parameters.
    self.azimuth = pattern.azimuth
    self.elevation = pattern.elevation
    self.depth = pattern.depth
    self.ppc = pattern.ppc

    self.ids.azimuth_slider.value = int(self.azimuth)
    self.ids.elevation_slider.value = int(self.elevation)
    self.ids.depth_slider.value = self.depth
    self.ids.ppc_slider.value = self.ppc
    self.ids.azimuth_input.value = "%d" % self.azimuth
    self.ids.elevation_input.value = "%d" % self.elevation
    self.ids.depth_input.value = "%.1f" % self.depth
    self.ids.ppc_input.value = "%.1f" % self.ppc

    self.UpdateAuxiliary()

    # Update pattern preview.
    self.mpl_a_pattern_preview.clear()
    self.mpl_a_pattern_preview.imshow(pattern.pattern)

    self.pattern_preview_canvas.draw()

  def PlacePattern(self):
    print("[PlacePattern]: start.")
    self.UpdateStatus("[PlacePattern]: start.")
    id_selected = self.ids.patterns_list.layout_manager.selected_nodes

    if len(id_selected) == 0:
      print("[PlacePattern]: no pattern selected.")
      self.UpdateStatus("[PlacePattern]: no pattern selected.")
      return
    
    pattern = self.patterns_on_the_list[id_selected[0]]
    pattern_wrapped = WrapPattern(self.vr_image, pattern.pattern, math.radians(pattern.azimuth), math.radians(-pattern.elevation),
                                  ipd=self.ipd, distance=pattern.depth, scale_meter_per_pixel=0.01 / pattern.ppc)
    

    print("[PlacePattern]: pattern wrapped.")
    self.UpdateStatus("[PlacePattern]: pattern wrapped.")

    if len(self.patterns_applied) > 0:
      AlphaBlend(self.patterns_applied[-1], pattern_wrapped, pattern_wrapped)

    print("[PlacePattern]: pattern blended for preview.")
    self.UpdateStatus("[PlacePattern]: pattern blended for preview.")

    self.patterns_applied.append(pattern_wrapped)

    self.UpdatePreview()

    print("[PlacePattern]: done.")
    self.UpdateStatus("[PlacePattern]: done.")

  def UndoPlacePattern(self):
    if len(self.patterns_applied) > 0:
      self.patterns_applied.pop()
      self.UpdatePreview()
      print("[UndoPlacePattern]: done.")
      self.UpdateStatus("[UndoPlacePattern]: done.")
    else:
      print("[UndoPlacePattern]: nothing to undo.")
      self.UpdateStatus("[UndoPlacePattern]: nothing to undo.")

  def ExportPreview(self):
    content = SaveDialog(save=self.export_preview, cancel=self.dismiss_popup)
    self._popup = Popup(title="Save preview to file", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def export_preview(self, path, filename):
    print("[ExportPreview]: start, export to", os.path.join(path, filename))
    self.UpdateStatus("[ExportPreview]: start.")
    try:
      cv2.imwrite(os.path.join(path, filename),
                  cv2.cvtColor(self.image_blended, cv2.COLOR_RGBA2BGRA))
      print("[ExportPreview]: done.")
      self.UpdateStatus("[ExportPreview]: done.")
    except:
      print("[ExportPreview]: failed.")
      self.UpdateStatus("[ExportPreview]: failed.")
    self.dismiss_popup()

  def BatchJobSelectInputDir(self):
    content = LoadDialog(load=self.batch_job_select_input_dir, cancel=self.dismiss_popup)
    self._popup = Popup(title="Select input dir", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def batch_job_select_input_dir(self, path, filename):
    input_dir = ""
    if len(filename) > 0:
      input_dir = os.path.dirname(filename[0])
    else:
      input_dir = path
    
    self.ids.inputdir_input.text = input_dir

    print("[BatchJobSelectInputDir]: selected to '%s'" % input_dir)
    self.UpdateStatus("[BatchJobSelectInputDir]: selected.")

    self.dismiss_popup()

  def BatchJobSelectOutputDir(self):
    content = LoadDialog(load=self.batch_job_select_output_dir, cancel=self.dismiss_popup)
    self._popup = Popup(title="Select output dir", content=content,
                        size_hint=(0.4, 0.8))
    self._popup.open()

  def batch_job_select_output_dir(self, path, filename):
    output_dir = ""
    if len(filename) > 0:
      output_dir = os.path.dirname(filename[0])
    else:
      output_dir = path

    print("[BatchJobSelectOutputDir]: selected to '%s'" % output_dir)
    self.UpdateStatus("[BatchJobSelectOutputDir]: selected.")

    if len(glob.glob(os.path.join(output_dir, "*"))) > 0:
      print("[BatchJobSelectOutputDir]: WARNING: output dir not empty.")
      self.UpdateStatus("[BatchJobSelectOutputDir]: WARNING non-empty.")
    
    self.ids.outputdir_input.text = output_dir
    self.dismiss_popup()

  def RunCore(self):
    print("[BatchJobRun]: start.")
    self.UpdateStatus("[BatchJobRun]: start.")
    if len(self.patterns_applied) == 0:
      print("[BatchJobRun]: ERROR: no patterns applied yet.")
      self.UpdateStatus("[BatchJobRun]: ERROR: no patterns being placed yet.")
      return

    input_dir = self.ids.inputdir_input.text
    input_file_pattern = os.path.join(input_dir, "*.*") if "*" not in input_dir else input_dir
    output_dir = self.ids.outputdir_input.text

    input_files = glob.glob(input_file_pattern)
    n_files = len(input_files)

    self.ids.pbar.max = n_files

    n_success = 0

    print("[BatchJobRun]: found %d files under input dir '%s'." % (n_files, input_dir))
    self.UpdateStatus("[BatchJobRun]: found %d files under input dir." % n_files)

    for i, img_file in enumerate(input_files):
      try:
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        n_channels = img.shape[2]
        if n_channels == 1:
          img_RGBA = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
        elif n_channels == 3:
          img_RGBA = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        elif n_channels == 4:
          img_RGBA = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
          raise Exception("'%s' has %d channels, but expected 1, 3 or 4 channels." % img_file, n_channels)

        AlphaBlend(img_RGBA, self.patterns_applied[-1], img_RGBA)

        output_filename = os.path.join(output_dir, os.path.basename(img_file))
        cv2.imwrite(output_filename, cv2.cvtColor(img_RGBA, cv2.COLOR_RGBA2BGR))

        print("[BatchJobRun]: working %d/%d." % (i + 1, n_files))
        self.UpdateStatus("[BatchJobRun]: working %d/%d." % (i + 1, n_files))
        n_success += 1
      except:
        print("[BatchJobRun]: ERROR: '%s' is not a readable image file, skipped." % img_file)
      self.ids.pbar.value = i + 1

    print("[BatchJobRun]: %d/%d done." % (n_success, n_files))
    self.UpdateStatus("[BatchJobRun]: %d/%d done." % (n_success, n_files))
    self.ids.pbar.value = 0

  def BatchJobRun(self):

    import threading
    mythread = threading.Thread(target=self.RunCore)
    mythread.start()

  def dismiss_popup(self):
    self._popup.dismiss()

  # def Load(self):
  #   content = LoadDialog(load=self.load_img, cancel=self.dismiss_popup)
  #   self._popup = Popup(title="Load file", content=content,
  #                       size_hint=(0.4, 0.8))
  #   self._popup.open()

  # def load(self, path, filename):
  #   # Implementation
  #   pass 
  #   self.dismiss_popup()

  # def Save(self):
  #   content = SaveDialog(save=self.save_img, cancel=self.dismiss_popup)
  #   self._popup = Popup(title="Save file", content=content,
  #                       size_hint=(0.4, 0.8))
  #   self._popup.open()

  # def save_img(self, path, filename):
  #   # Implementation
  #   pass 
  #   # cv2.imwrite(os.path.join(path, filename),
  #   #             cv2.cvtColor(self.GeneratePreview(), cv2.COLOR_RGBA2BGRA))
  #   self.dismiss_popup()

class AddPatternsApp(App):
  def build(self):
    Window.size = (1500, 900)
    return AddPatterns()


Factory.register('AddPatterns', cls=AddPatterns)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == "__main__":
  AddPatternsApp().run()