#!/usr/bin/env python
import sys
import copy

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import os
from sys import exit as exit

# Simple Image Browser based on PySimpleGUI

# Get the folder containing the images from the user
folder = '/Users/yanjingang/tmp/test'
folder = sg.PopupGetFolder(message='Image folder to open', title='选择png图片目录', default_path=folder)
if folder is None:
    sg.PopupCancel('Cancelling')
    exit(0)

# get list of PNG files in folder
png_files = [folder + '/' + f for f in os.listdir(folder) if '.png' in f]
file_names = [f for f in os.listdir(folder) if '.png' in f]
print(png_files)
print(file_names)

if len(png_files) == 0:
    sg.Popup('No PNG images in folder')
    exit(0)

# define menu layout
#menu = [['File', ['Open Folder', 'Exit']], ['Help', ['About', ]]]
#col_files = [[sg.Listbox(values=file_names, size=(60, 30), key='listbox')], [sg.Button('Read')]]
menu = [['File', ['Exit']], ['Help', ['About', ]]]
col_files = [[sg.Listbox(values=file_names, size=(60, 30), key='listbox')]]
# define layout, show and read the window
col = [[sg.Text(png_files[0], size=(80, 3), key='filename')],
       [sg.Image(filename=png_files[0], key='image')],
       [sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2)),
        sg.Text('File 1 of {}'.format(len(png_files)), size=(15, 1), key='filenum')]]

layout = [[sg.Menu(menu)], [sg.Column(col_files), sg.Column(col)]]
print(menu)
print(col_files)
print(col)
window = sg.Window('图片播放器', return_keyboard_events=True, location=(0, 0), use_default_focus=False).Layout(layout)

# loop reading the user input and displaying image, filename
i = 0
while True:

    event, values = window.Read()
    # --------------------- Button & Keyboard ---------------------
    if event is None:
        break
    elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34') and i < len(png_files) - 1:
        i += 1
    elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33') and i > 0:
        i -= 1
    elif event == 'Exit':
        exit(69)

    filename = folder + '/' + values['listbox'][0] if event == 'Read' else png_files[i]
    print(filename)

    # ----------------- Menu choices -----------------
    '''if event == 'Open Folder':
        newfolder = sg.PopupGetFolder('New folder', no_window=True)
        if newfolder is None:
            continue
        folder = newfolder
        png_files = [folder + '/' + f for f in os.listdir(folder) if '.png' in f]
        file_names = [f for f in os.listdir(folder) if '.png' in f]
        window.FindElement('listbox').Update(values=file_names)
        window.Refresh()
        i = 0
    el'''
    if event == 'About':
        sg.Popup('Demo PNG Viewer Program', 'Please give PySimpleGUI a try!')

    # update window with new image
    window.FindElement('image').Update(filename=filename)
    # update window with filename
    window.FindElement('filename').Update(filename)
    # update page display
    window.FindElement('filenum').Update('File {} of {}'.format(i + 1, len(png_files)))
