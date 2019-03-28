# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""

import colorsys
import os
import cv2
from timeit import default_timer as timer
import requests
import numpy as np
from keras import backend as K
from keras.models import load_model, Model
from keras.layers import Input, Lambda
from keras.utils import multi_gpu_model
from keras.optimizers import Adam
from PIL import Image, ImageDraw
from ....lib.yolo_v3.model import yolo_eval, yolo_body, tiny_yolo_body, yolo_loss, preprocess_true_boxes
from ....lib.yolo_v3.utils import letterbox_image, get_random_data
from ...application import Application

class YOLO_V3(Application):
    def __init__(self, input_shape = None):
        if type(input_shape) != type(None):            
            self.input_shape = input_shape
        Application.__init__(self)
        self.anchors = np.array([10.0,13.0, 16.0,30.0, 33.0,23.0, 30.0,61.0, 62.0,45.0, 59.0,119.0, 116.0,90.0, 156.0,198.0, 373.0,326.0]).reshape(-1,2)
        self.sess = K.get_session()
        self.model_image_size = (416,416)

    def prepare_train_data(self, data_path = None, get_image_from = 'directory', data_array = None, classes_path = None, annotation_path = None, gpu_num = 1):
        self.data_path = data_path
        self.get_image_from = get_image_from
        self.data_array = data_array
        self.annotation_path = annotation_path
        self.gpu_num = gpu_num
        self.class_names = self.get_classes(classes_path)

        if get_image_from == 'directory':
            assert data_path, "Provide data_path to train from directory"
        elif get_image_from == 'argument':
            assert data_array, "Provide data_array to train from argument"
        else:
            raise ValueError("value of get_image_from should be either 'directory' or 'argument'.")

    def save(self, output_model_path):
        derived_model = Model(self.yolo_model.input[0], [self.yolo_model.layers[249].output, self.yolo_model.layers[250].output, self.yolo_model.layers[251].output])
        derived_model.save(output_model_path)
        print("saved model to " + output_model_path)

    def download_trained_weights(self, weights_path):
        print("Downloading pretrained model to " + weights_path + " ...")
        URL = "https://drive.google.com/uc?export=download"
        id = "1Dd-uUhhXvosXiIIZM8tiXoZyENJxIY4u"
        session = requests.Session()

        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)

        CHUNK_SIZE = 32768

        with open(weights_path, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        print("... done downloading pretrained model!")
        
    def create_model(self, input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2, weights_path=None):
        '''create the training model'''
        K.clear_session() # get a new session
        image_input = Input(shape=(None, None, 3))
        h, w = input_shape
        num_anchors = len(anchors)

        # y_true = [Input(shape=(416//{0:32, 1:16, 2:8}[l], 416//{0:32, 1:16, 2:8}[l], 9//3, 80+5)) for l in range(3)]
        y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], num_anchors//3, num_classes+5)) for l in range(3)]

        model_body = yolo_body(image_input, num_anchors//3, num_classes)
        print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

        if load_pretrained:
            if not os.path.exists(weights_path):
                self.download_trained_weights(weights_path)
            model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
            print('Load weights {}.'.format(weights_path))
            if freeze_body in [1, 2]:
                # Freeze darknet53 body or freeze all but 3 output layers.
                num = (185, len(model_body.layers)-3)[freeze_body-1]
                for i in range(num): model_body.layers[i].trainable = False
                print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

        model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
            arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
            [*model_body.output, *y_true])
        model = Model([model_body.input, *y_true], model_loss)
        print('model_body.input: ', model_body.input)
        print('model.input: ', model.input)

        return model

    def train(self, epochs = 10, batch_size = 32, weights_path = None):
        # return
        num_classes = len(self.class_names)
        anchors = self.anchors

        input_shape = (416,416) # multiple of 32, hw
        if hasattr(self, 'input_shape'):
            input_shape = self.input_shape

        is_tiny_version = len(anchors)==6 # default setting
        if is_tiny_version:
            model = self.create_tiny_model(input_shape, anchors, num_classes,
                freeze_body=2, weights_path=weights_path)
        else:
            model = self.create_model(input_shape, anchors, num_classes,
                freeze_body=2, weights_path=weights_path) # make sure you know what you freeze
        # model.save('yolo_model_retrain.h5')  # creates a HDF5 file 'my_model.h5'

        print(model.input)
        print(model.output)

        val_split = 0.1
        with open(self.annotation_path) as f:
            lines = f.readlines()
        np.random.seed(10101)
        np.random.shuffle(lines)
        np.random.seed(None)
        num_val = int(len(lines)*val_split)
        num_train = len(lines) - num_val


        # Train with frozen layers to get a stable loss.
        model.compile(optimizer=Adam(lr=1e-3), loss='mean_squared_error')

        print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
        model.fit_generator(self.data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes),
                steps_per_epoch=max(1, num_train//batch_size),
                validation_data=self.data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors, num_classes),
                validation_steps=max(1, num_val//batch_size),
                epochs=epochs,
                initial_epoch=0,
                callbacks=[])
        self.yolo_model = model

    def data_generator(self, annotation_lines, batch_size, input_shape, anchors, num_classes):
        '''data generator for fit_generator'''
        n = len(annotation_lines)
        i = 0
        while True:
            image_data = []
            box_data = []
            for b in range(batch_size):
                if i==0:
                    np.random.shuffle(annotation_lines)
                image, box = get_random_data(annotation_lines[i], input_shape, random=True)
                image_data.append(image)
                box_data.append(box)
                i = (i+1) % n
            image_data = np.array(image_data)   # input of original yolo: image
            box_data = np.array(box_data)       # output of original yolo: boxes
            y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes) # some kind of output description?!
            yield [image_data, *y_true], np.zeros(batch_size)

    def data_generator_wrapper(self, annotation_lines, batch_size, input_shape, anchors, num_classes):
        n = len(annotation_lines)
        if n==0 or batch_size<=0:
            return None
        return self.data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes)

    def create_tiny_model(self, input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
                weights_path='model_data/tiny_yolo_weights.h5'):
        '''create the training model, for Tiny YOLOv3'''
        K.clear_session() # get a new session
        image_input = Input(shape=(None, None, 3))
        h, w = input_shape
        num_anchors = len(anchors)

        y_true = [Input(shape=(h//{0:32, 1:16}[l], w//{0:32, 1:16}[l], \
            num_anchors//2, num_classes+5)) for l in range(2)]

        model_body = tiny_yolo_body(image_input, num_anchors//2, num_classes)
        print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

        if load_pretrained:
            model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
            print('Load weights {}.'.format(weights_path))
            if freeze_body in [1, 2]:
                # Freeze the darknet body or freeze all but 2 output layers.
                num = (20, len(model_body.layers)-2)[freeze_body-1]
                for i in range(num): model_body.layers[i].trainable = False
                print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

        model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
            arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})(
            [*model_body.output, *y_true])
        model = Model([model_body.input, *y_true], model_loss)

        return model

    def get_classes(self, classes_path):
        '''loads the classes'''
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names
    def generate(self, model_path = None, score_threshold = 0.3, iou_threshold = 0.45):
        model_path = os.path.expanduser(model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            print('output_shape = %d' %(self.yolo_model.layers[-1].output_shape[-1]))
            print('num_anchors = %d' % num_anchors)
            print('len = %d' %(len(self.yolo_model.output) * (num_classes + 5)))
            print('len_output = %d' %(len(self.yolo_model.output)))
            assert self.yolo_model.layers[-1].output_shape[-1] == num_anchors/len(self.yolo_model.output) * (num_classes + 5), 'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
        self.boxes, self.scores, self.classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=score_threshold, iou_threshold=iou_threshold)

    def detect_image(self, image):
        image = Image.open(image)
        self._detect_image(image)
        self.sess.close()

    def _detect_image(self, image):
        start = timer()

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        print(image_data.shape)
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })

        print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

        thickness = (image.size[0] + image.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            print(label, (left, top), (right, bottom))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=self.colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self.colors[c])
            print(text_origin.shape)
            draw.text(list(text_origin), label, fill=(0, 0, 0))
            del draw

        end = timer()
        print(end - start)
        image.show()

        return image
    
    def save_image(self, image, output_path):
        opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, opencvImage)

    def detect_video(self, video_path, output_path=""):
        vid = cv2.VideoCapture(video_path)
        print('vid: ', vid)
        print('output_path: ', output_path)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")
        video_FourCC    = cv2.VideoWriter_fourcc(*"mp4v")
        video_fps       = vid.get(cv2.CAP_PROP_FPS)
        video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        isOutput = True if output_path != "" else False
        if isOutput:
            print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
            out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
        accum_time = 0
        curr_fps = 0
        fps = "FPS: ??"
        prev_time = timer()
        while True:
            return_value, frame = vid.read()
            if not return_value:
                break
            image = Image.fromarray(frame)
            image = self._detect_image(image)
            result = np.asarray(image)
            curr_time = timer()
            exec_time = curr_time - prev_time
            prev_time = curr_time
            accum_time = accum_time + exec_time
            curr_fps = curr_fps + 1
            if accum_time > 1:
                accum_time = accum_time - 1
                fps = "FPS: " + str(curr_fps)
                curr_fps = 0
            cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 0, 0), thickness=2)
            cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow("result", result)
            if isOutput:
                out.write(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.sess.close()