#########################################################################
#
# Copyright (C) 2019 Team Deep-Data, Colorado School of Mines
#
# Date created: 1/22/19
# Date last updated:
#
# Creators:
#   - Sean Smith            seansmith@mines.edu
#   - Tyler Murphy          tmurphy@mines.edu
#   - Tyler Blount          trblount@mines.edu
#   - Sydney Nelson         snelson1@mines.edu
#   - Josh Grego            jgrego@mines.edu
#   - Jake Steiner          msteiner@mines.edu
#   - Marcelo Gonzales      magonzal@mines.edu
#   - Daniel Hanuszczak     danielhanuszczak@mines.edu
#
#########################################################################

'''
Module for mapping band ratio output arrays

Methods:
    create_heatmap_interactive

'''

import os
import errno
import numpy as np
import builtins
import time
from skimage import io
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib import ticker
from rasterio import plot
import logging


################################################################################
###                             HELPER FUNCTIONS                             ###
################################################################################
def normalize(array):
    max_value = np.max(array)
    min_value = np.min(array)
    array = (array - min_value) / (max_value - min_value)
    return array



################################################################################
###                                 HEATMAP                                  ###
################################################################################
def create_heatmap_interactive(
    band_reader,
    bandratio_array,
    bandratio_array_name,
    flight_name,
    alpha = 0.6,
    gamma_1 = False,
    interval = 0.00001,
    std_multiplier = 3,
    clipped = False,
    display = True,
    save = False,
    cmap = 'hot',
    quiet = False,
    rgb_scale_value = None
    ):

    '''
        Function for creating an interactive heatmap

        Reference ==============================================================
            N/A

        Inputs =================================================================
            band_reader - band_reader class instance
            bandratio_array - bandratio result array for heatmap
            bandratio_array_name - name of bandratio calculated
            flight_name - name of the flight
            alpha - transparency value of overlay (Defualt 0.6)
            gamma_1 - threshold value for map (Default mean of normalized bandratio_array)
            interval - step value of threshold slider (Default 0.00001)
            std_multiplier - multiplier of std for range of values of threshold slider (Default 3)
            clipped - if want clipped heatmap instead of default treshhold (Default False)
            display - show plt (Default True)
            save - save plt when (Default False)
            cmap - color scheme for heatmap (Default 'hot' for threshold, 'jet' for clipped)
            quiet - if should not log info about bandratio_array (Defualt False)
            rgb_scale_value - float value to increase brightness of rgb image

        Returns ================================================================
            N/A

    '''
    
    if clipped: cmap = 'jet'

    if band_reader.mode == 'aviris' or band_reader.mode == 'pickled_aviris':
        mode = 'AVIRIS'
        if rgb_scale_value is None: rgb_scale_value = 8
    elif band_reader.mode == 'hyperion':
        mode = 'Hyperion'
        if rgb_scale_value is None: rgb_scale_value = 2
    else:
        raise ValueError('Mapper does not recignize band_reader mode: {}'.format(band_reader.mode))

    rgb = ['652', '542', '471']
    r = normalize(band_reader.load_band(rgb[0], False))
    g = normalize(band_reader.load_band(rgb[1], False))
    b = normalize(band_reader.load_band(rgb[2], False))
    image = np.stack([r, g, b], axis=2)

    height = image.shape[0]
    width = image.shape[1]

    # normalize heat map
    max_value = np.max(bandratio_array)
    min_value = np.min(bandratio_array)

    normalized_heat_map = normalize(bandratio_array)
    normalized_heat_map = normalized_heat_map.squeeze()
    m = normalized_heat_map.mean()
    std = normalized_heat_map.std()

    if not quiet:
        logging.info('-> bandratio_array name: {}'.format(bandratio_array_name))
        logging.info('-> bandratio_array mean: {}'.format(bandratio_array.mean()))
        logging.info('-> bandratio_array max: {}'.format(max_value))
        logging.info('-> bandratio_array min: {}'.format(min_value))
        logging.info('-> normalized_heat_map mean: {}'.format(m))
        logging.info('-> normalized_heat_map std: {}'.format(normalized_heat_map.std()))

    if not gamma_1: gamma_1 = np.copy(m)


    # fig, axs = plt.subplots(1,3)
    axs = [0, 0, 0]
    fig = plt.figure()
    axs[0] = plt.subplot(1,3,1)
    axs[1] = plt.subplot(1,3,2, sharex=axs[0], sharey=axs[0])
    axs[2] = plt.subplot(1,3,3)

    axs[0].set_title('Original')
    axs[0].set_ylabel('Mean: {:.5f}'.format(m))
    axs[0].imshow(np.clip(image*rgb_scale_value, 0, 1))
    axs[1].imshow(np.clip(image*rgb_scale_value, 0, 1))

    # SPECRUM PLOT
    axs[2].set_title('Spectrum Plot')
    axs[2].set_ylabel('Irradience')
    axs[2].set_xlabel('Band')
    axs[2].xaxis.set_major_locator(ticker.MaxNLocator(5))

    # SPECTRAL PLOT IN NEW WINDOW
    # fig1, axs1 = plt.subplots()
    # axs1.set_title('Spectrum Plot')
    # axs1.set_ylabel('Irradience')
    # axs1.set_xlabel('Band')


    if clipped:
        fig.suptitle('{} Heatmap: {} | Clipped | alpha: {:.2f}'.format(mode, bandratio_array_name, alpha), fontsize=16)

        # OVERLAY CLIPPED IMAGES
        axs[1].set_title('Clipped')
        axs[1].set_ylabel('Gamma: {:.5f}'.format(gamma_1))
        axs[1].imshow(image)
        vec_1 = normalize(np.clip(np.copy(normalized_heat_map), m - (std * gamma_1), m + (std * gamma_1)))
        axs[1].imshow(vec_1, alpha=alpha, cmap=cmap)

        amp_slider_ax  = fig.add_axes([0.12, 0.01, 0.65, 0.03])
        amp_slider = Slider(amp_slider_ax, 'Threshold', 0, 1, valinit=gamma_1, valstep=interval, valfmt='%1.5f')

        # Define an action for modifying the line when any slider's value changes
        def sliders_on_changed(val):
            vec_1 = normalize(np.clip(np.copy(normalized_heat_map), m - amp_slider.val, m + amp_slider.val))
            axs[1].imshow(vec_1, alpha=alpha, cmap=cmap)
        amp_slider.on_changed(sliders_on_changed)

    else:
        # OVERLAY THRESHOLD IMAGES
        fig.suptitle('{} Heatmap: {} | Threshold | alpha: {:.2f}'.format(mode, bandratio_array_name, alpha), fontsize=16)

        axs[1].set_title('Threshold')
        axs[1].set_ylabel('Threshold Default: {:.5f}'.format(gamma_1))

        vec_1 = np.copy(normalized_heat_map)
        vec_1[vec_1 >= gamma_1] = 1
        vec_1[vec_1 < gamma_1] = 0
        a = axs[1].imshow(vec_1, alpha=alpha, cmap=cmap, interpolation='nearest')

        amp_slider_ax  = fig.add_axes([0.12, 0.01, 0.65, 0.03])
        amp_slider = Slider(amp_slider_ax, 'Threshold', (m-(std_multiplier*std)), (m+(std_multiplier*std)), valinit=gamma_1, valstep=interval, valfmt='%1.5f')

        # Define an action for modifying the line when any slider's value changes
        def sliders_on_changed(val):
            vec_1 = np.copy(normalized_heat_map)
            vec_1[vec_1 >= amp_slider.val] = 1
            vec_1[vec_1 < amp_slider.val] = 0
            axs[1].imshow(vec_1, alpha=alpha, cmap=cmap, interpolation='nearest')
        amp_slider.on_changed(sliders_on_changed)

    # Add a button for resetting the parameters
    reset_button_ax = fig.add_axes([0.85, 0.01, 0.1, 0.04])
    reset_spectrum_plot_ax = fig.add_axes([0.88, 0.9, 0.1, 0.04])

    reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975')
    reset_spectrum_plot = Button(reset_spectrum_plot_ax, 'Clear Plot', hovercolor='0.975')

    def reset_button_on_clicked(mouse_event):
        amp_slider.reset()
    reset_button.on_clicked(reset_button_on_clicked)

    def reset_spectrum_plot_on_clicked(mouse_event):
        axs[2].get_legend().remove()
        axs[2].lines = []
    reset_spectrum_plot.on_clicked(reset_spectrum_plot_on_clicked)

    # SPECTRUM PLOT IN SAME WINDOW
    def on_click(event):
        axs[0].time_on_click = time.time()
    def on_release(event):
        # Only clicks inside this axis are valid.
        if event.inaxes in [axs[0], axs[1]]:
            if event.button == 1 and ((time.time() - axs[0].time_on_click) < 0.15):
                result_dict = band_reader.load_pixel(int(event.ydata), int(event.xdata))
                axs[2].plot(*zip(*result_dict.items()), label='Row: {}, Col: {}'.format(int(event.ydata), int(event.xdata)))
                axs[2].legend()
                fig.canvas.draw()

    # SPECTRAL PLOT IN NEW WINDOW
    # def on_pixel_click(event):
    #     logging.info('Loading Row: {}, Col: {}'.format(int(event.ydata), int(event.xdata)))
    #     result_dict = band_reader.load_pixel(int(event.ydata), int(event.xdata))
    #     logging.info('Done.')
    #     axs1.xaxis.set_major_locator(ticker.MaxNLocator(5))
    #     axs1.set_title('Spectral Plot, Row: {}, Col: {}'.format(int(event.ydata), int(event.xdata)))
    #     axs1.plot(*zip(*sorted(result_dict.items())))
    #
    #     fig1.canvas.draw()
    #     fig1.show()
    # cid = fig.canvas.mpl_connect('button_press_event', on_pixel_click)

    cid0 = fig.canvas.mpl_connect('button_press_event', on_click)
    cid1 = fig.canvas.mpl_connect('button_release_event', on_release)

    if display:
        plt.show()
    if save:
        fn = bandratio_array_name + '_heatmap.png'
        save_path = os.path.join(os.path.dirname(os.getcwd()), fn)
        logging.info('-> Saving heatmap to: {}'.format(save_path))
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
