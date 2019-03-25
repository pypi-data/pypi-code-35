import os
import json
import numpy as np
import skimage.draw
import random
import skimage.io
from ...application import Application

# Import Mask RCNN
from mrcnn import model as modellib, utils, visualize
from mrcnn.config import Config

# Getting number of avaialbe gpus
from tensorflow.python.client import device_lib


class Mask_RCNN(Application):
    def __init__(self, class_list_path = None, weights_path = None, backbone = None):
        super().__init__()

        self.config = CustomConfig()
        if type(backbone) != type(None):
            self.config.BACKBONE = backbone
        if type(weights_path) == type(None):
            self.config.GPU_COUNT = self.gpu_num
            self.config.BATCH_SIZE = self.config.GPU_COUNT * self.config.IMAGES_PER_GPU      
        elif type(class_list_path) == type(None):
            raise ValueError("you should write class list and weights_path both")
        else :
            self.config.GPU_COUNT = 1
            self.config.IMAGES_PER_GPU = 1
            self.config.BATCH_SIZE = self.config.GPU_COUNT * self.config.IMAGES_PER_GPU
            self.load_model(class_list_path, weights_path)


    def create_model(self, mode = "training") :
        self.model = modellib.MaskRCNN(mode= mode, config=self.config, model_dir='.' )
        self.model.config.display()


    def prepare_train_data(self, get_image_from = 'directory', data_path = None, data_array = None, exist_weights_path = None):
        self.get_image_from = get_image_from
        self.data_path = data_path
        self.data_array = data_array

        if get_image_from == 'directory':
            assert data_path, "Provide data_path to train from directory"
        elif get_image_from == 'argument':
            assert data_array, "Provide data_array to train from argument"
        else:
            raise ValueError("value of get_image_from should be either 'directory' or 'argument'.")

        self.dataset_train = ImageDataset()
        self.dataset_train.load_class(self.data_path, "train")
        self.dataset_train.prepare()
        print("Images: {}\nClasses: {}".format(len(self.dataset_train.image_ids), self.dataset_train.class_names))

        self.dataset_val = ImageDataset()
        self.dataset_val.load_class(self.data_path, "val")
        self.dataset_val.prepare()
        print("Images: {}\nClasses: {}".format(len(self.dataset_val.image_ids), self.dataset_val.class_names))
        
        assert sorted(self.dataset_train.class_names) == sorted(self.dataset_val.class_names), "train classes have to be same with val classes"

        self.setConfig(class_list = self.dataset_train.class_names)

        self.create_model(mode = "training")

    
    def train(self, weights_path = None, learning_rate = 0.01, epochs = 4, layers = 'heads') :
        # Use pretrained weights if exist weights path not given.
        if type(weights_path) == type(None) :
            weights_path = 'coco.h5'
            if not os.path.exists('coco.h5'):
                utils.download_trained_weights(weights_path)
        
        # Load weights
        print("Loading weights ", weights_path)

        self.model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
            
        self.model.train(self.dataset_train, self.dataset_val,
            learning_rate = learning_rate,
            epochs = epochs,
            layers = layers)


    def save(self, class_list_path, weights_path) : 
        self.model.keras_model.save_weights(weights_path)
        with open(class_list_path, 'w') as f:
            for i in range(self.config.NUM_CLASSES):
                f.write("%s" % self.config.CLASS_NAMES[i])
                i += 1
                if i != self.config.NUM_CLASSES :
                    f.write("\n")


    def load_model(self, class_list_path = None, weights_path = None):
        if type(class_list_path) == None : 
            raise ValueError("Class names should be given")     
        if type(weights_path) == None : 
            raise ValueError("Weights path should be given")     

        class_file = open(class_list_path, 'r')
        class_objects = class_file.read()
        class_file.close()
        class_list = class_objects.split('\n')
        #remove last class_list
        self.setConfig(class_list = class_list)
        self.create_model(mode = "inference") 
        print("Loading weights from ", weights_path)
        self.model.load_weights(weights_path, by_name=True)
        print("testMemory")
        

    def predict(self, data_array = None, data_path = None, predict_classes = True, verbose = 0, steps = None, use_coco_config = False):
        if data_path :
            try:
                predict_image = skimage.io.imread(data_path)
                _, filename = os.path.split(data_path)
            except Exception as e:
                raise e

        results = self.model.detect([predict_image], verbose = 1)
        r = results[0]
        image_data = [predict_image]

        self.mask(image_data = image_data, r = r)


    def setConfig(self, class_list, detection_threshold = 0.8, backbone = 'resnet50') :
        self.config.CLASS_NAMES = class_list
        self.config.NUM_CLASSES = len(class_list)
        self.config.IMAGE_META_SIZE = 12 + self.config.NUM_CLASSES
        self.config.DETECTION_MIN_CONFIDENCE = detection_threshold
        self.config.BACKBONE = backbone


    def mask(self, image_data, r, show_mask = True):
        visualize.display_instances(image_data[0], r['rois'], r['masks'], r['class_ids'],
                                    self.config.CLASS_NAMES, r['scores'], show_mask = show_mask)


class ImageDataset(utils.Dataset):
    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "source":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a shape dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "source":
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1
        # Return mask, and array of class IDs of each instance.
        if info["class_ids"]:
            class_ids = np.array(info["class_ids"], dtype = np.int32)
            return mask.astype(np.bool), class_ids
        else:
            return super(self.__class__, self).load_mask(image_id)
    
    def load_class(self, dataset_dir, subset):
        """Load a subset of the dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Train or validation dataset?
        assert subset in ["train", "val"]

        dataset_dir = os.path.join(dataset_dir, subset)

        # Load annotations
        # VGG Image Annotator (up to version 1.6) saves each image in the form:
        # { 'filename': '28503151_5b5b7ec140_b.jpg',
        #   'regions': {
        #       '0': {
        #           'region_attributes': {},
        #           'shape_attributes': {
        #               'all_points_x': [...],
        #               'all_points_y': [...],
        #               'name': 'polygon'}},
        #       ... more regions ...
        #   },
        #   'size': 100202
        # }
        # We mostly care about the x and y coordinates of each region
        # Note: In VIA 2.0, regions was changed from a dict to a list.
        annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]
        class_list = []
        # Get classes in json files first
        for a in annotations:
            class_ids = []
            if type(a['regions']) is dict:
                for r in a['regions'].values():
                    c = r['region_attributes']['class']
                    if c not in class_list:
                        class_list.append(c)
            else:
                for r in a['regions']:
                    c = r['region_attributes']['class']
                    if c not in class_list:
                        class_list.append(c)
                        
        # After getting classes sort for making same class_list of train, val data
        class_list.sort()
        # put class_list names into self j should be start with 1 because of bg class
        j = 1
        for class_name in class_list:
            self.add_class("source", j, class_name)
            j += 1

        # After getting classes get polygons and give class ids of polygons
        for a in annotations:
            class_ids = []
            if type(a['regions']) is dict:
                polygons = []
                for r in a['regions'].values():
                    polygons.append(r['shape_attributes'])
                    c = r['region_attributes']['class']
                    class_ids.append(class_list.index(c) + 1)
            else:
                polygons = []
                for r in a['regions']:
                    polygons.append(r['shape_attributes'])
                    c = r['region_attributes']['class']
                    class_ids.append(class_list.index(c) + 1)
        

            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "source",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width, height=height,
                polygons=polygons,
                class_ids = class_ids)


############################################################
#  Configurations
############################################################


class CustomConfig(Config):
    """Configuration for training on the custom dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name 
    # TODO: have to change Name of config for log etc.
    NAME = "CUSTOMMRCNN"

    # Number of classes (including background)
    NUM_CLASSES = 1  # Background + classes

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 50

    # Skip detections with < 60% confidence
    DETECTION_MIN_CONFIDENCE = 0.8

    # Names of classes
    CLASS_NAMES = []

    IMAGE_META_SIZE = 13

    BATCH_SIZE = 1

    # BACKBONE should be resnet 50 or resnet 101
    BACKBONE = "resnet50"

    # params to reduce memory
    TRAIN_ROIS_PER_IMAGE = 100
    IMAGES_PER_GPU = 1
    MAX_GT_INSTANCES = 30
