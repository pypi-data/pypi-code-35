import sys
import os
import cv2
import numpy as np

""" Load cascade xml file and save to FACE_CASCADE
"""
FACE_CASCADE = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

def extract_face(image_path,
                scale_factor=1.1,
                min_neighbors=5,
                output_directory=None,
                output_prefix=None):
    """ Extract the human face from image and return number of detected face
    image_path -- The path of the image.
    scale_factor -- Specifying how much the image size is reduced at each image scale (default 1.1).
    min_neighbors -- Specifying how many neighbors each candidate rectangle should have to retain it (default 5).
    output_directory -- Directory where to save output (default None - same as input image)
    output_prefix -- Prefix of output (default None - the name of input image)
    """

    
    if not os.path.exists(image_path):
        """ If given image file does not exist
        """
        raise FileNotFoundError("Happens when given file not exist")

    if not output_prefix:
        output_prefix = os.path.splitext(os.path.split(image_path)[1])[0]

    if not output_directory:
        output_directory = os.path.split(image_path)[0]
    else:
        if not os.path.exists(output_directory):
            try:
                os.mkdir(output_directory)
            except:
                raise PermissionError("Exception while creating directory")

    try:    
        img = cv2.imread(image_path)
    except:
        raise TypeError("Happens when given image not correct")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray_img, scale_factor, min_neighbors)
    
    width, height = img.shape[:2]
    count = 0
    for (x, y, w, h) in faces:
        y1 = int(y)
        y2 = int(y + h)
        x1 = int(x)
        x2 = int(x + w)
                
        if y1 < 0: y1 = 0

        if y2 > width: y2 = width

        if x1 < 0: x1 = 0

        if x2 > height: x2 = height

        crop_img = img[y1:y2, x1:x2]
        
        file_path = os.path.join(
                output_directory, output_prefix + '_' + str(count) + '_' + '.jpg')
        count = count + 1
        try:        
            cv2.imwrite(file_path, crop_img)
        except:
            raise PermissionError("Exception while creating new image")
        
    return len(faces)
        