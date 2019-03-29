import cv2
from .create_vr_mapping import CreateVRMapping
import numpy as np
import math

def WrapPattern(vr_image, pattern, azimuth, elevation,
                ipd=0.05, distance=10, scale_meter_per_pixel=0.0005):
  
  # Probe mapped size
  map1_right = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map2_right = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map1_left = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map2_left = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)

  CreateVRMapping(
    vr_image.shape[0], vr_image.shape[1],
    pattern.shape[0], pattern.shape[1],
    azimuth, elevation,
    map1_right, map2_right, map1_left, map2_left,
    ipd=ipd, distance=distance, scale_meter_per_pixel=scale_meter_per_pixel)
  
  text_in_vr = np.zeros((vr_image.shape[0], vr_image.shape[1], 4), np.uint8)
  text_in_vr[text_in_vr.shape[0] // 2:,:,:] = cv2.remap(pattern, map1_right, map2_right, interpolation=cv2.INTER_LANCZOS4)
  text_in_vr[:text_in_vr.shape[0] // 2,:,:] = cv2.remap(pattern, map1_left, map2_left, interpolation=cv2.INTER_LANCZOS4)
  
  # Downsample
  dimension = math.sqrt(np.sum(np.sum(abs(text_in_vr - (0,0,0,0)), axis=2) > 0))
  scale = pattern.shape[1] / dimension / 3
  
  pattern_downsampled = cv2.resize(pattern,
                                   (int(pattern.shape[1] / scale), int(pattern.shape[0] / scale)),
                                   interpolation=cv2.INTER_AREA)
  
  # Wrap again
  map1_right = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map2_right = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map1_left = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)
  map2_left = np.zeros((vr_image.shape[0] // 2, vr_image.shape[1]), np.float32)

  CreateVRMapping(
    vr_image.shape[0], vr_image.shape[1],
    pattern_downsampled.shape[0], pattern_downsampled.shape[1],
    azimuth, elevation,
    map1_right, map2_right, map1_left, map2_left,
    ipd=ipd, distance=distance, scale_meter_per_pixel=scale_meter_per_pixel * scale)
  
  text_in_vr = np.zeros((vr_image.shape[0], vr_image.shape[1], 4), np.uint8)
  text_in_vr[text_in_vr.shape[0] // 2:,:,:] = cv2.remap(pattern_downsampled, map1_right, map2_right, interpolation=cv2.INTER_LANCZOS4)
  text_in_vr[:text_in_vr.shape[0] // 2,:,:] = cv2.remap(pattern_downsampled, map1_left, map2_left, interpolation=cv2.INTER_LANCZOS4)
  
  return text_in_vr