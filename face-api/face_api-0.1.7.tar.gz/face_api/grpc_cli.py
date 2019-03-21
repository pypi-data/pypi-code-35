# -*- coding: utf-8 -*-
# Face API client
# BIG CHENG, init 2019/03/20
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


from __future__ import print_function

import sys
import threading

import grpc
import numpy as np
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

import face_api.img_util as img_util


class _TaskSyncer(object):
  """Syncer for the prediction tasks."""

  def __init__(self, num_tests, concurrency):
    self._condition = threading.Condition()

    ## task control
    self._num_tests = num_tests
    self._done = 0

    self._fess = None ## result fes
    self._error = 0

    ## concurrency control
    self._concurrency = concurrency
    self._active = 0
    

  def wait_result(self):
    with self._condition:
      while self._done != self._num_tests:
        self._condition.wait()
      #return self._error / float(self._num_tests)
      
  def inc_done(self):
    with self._condition:
      self._done += 1
      self._condition.notify()

  def throttle(self):
    with self._condition:
      while self._active == self._concurrency:
        self._condition.wait()
      self._active += 1

  def dec_active(self):
    with self._condition:
      self._active -= 1
      self._condition.notify()
      
  def inc_error(self):
    with self._condition:
      self._error += 1

  def get_error_rate(self):
    with self._condition:
      while self._done != self._num_tests:
        self._condition.wait()
      return self._error / float(self._num_tests)

def _create_rpc_callback(label, task_syncer):
  """Creates RPC callback function.

  Args:
    label: The correct label for the predicted example.
    task_syncer: Counter for the prediction result.
  Returns:
    The callback function.
  """
  def _callback(result_future):
    """Callback function.

    Calculates the statistics for the prediction result.

    Args:
      result_future: Result future of the RPC.
    """
    exception = result_future.exception()
    if exception:
      task_syncer.inc_error()
      print("!!!")
      print(exception)
      response = None
    else:
      sys.stdout.write('.')
      sys.stdout.flush()
      response = np.array(
          result_future.result().outputs['embeddings'].float_val)
    
    task_syncer.inc_done()
    task_syncer.dec_active()  ## concurrency control   
    task_syncer._fess = response  ## store result
  return _callback



def do_inference(hostport, work_dir, concurrency, num_tests, model, signature, imgs):
  """Connect Face Recognition Service with concurrent requests.

  Args:
    hostport: Host:port address of the PredictionService.
    work_dir: The full path of working directory for test data set.
    concurrency: Maximum number of concurrent requests.
    num_tests: Number of test images to use.

  Returns:
    The Face Recognition description vector.

  Raises:
    IOError: An error occurred processing test data set.
  """
  channel = grpc.insecure_channel(hostport)
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  task_syncer = _TaskSyncer(num_tests, concurrency)
  ##task_syncer = _TaskSyncer(1, 1) ## run only 1

  for _ in range(num_tests):
    request = predict_pb2.PredictRequest()
    
    request.model_spec.name = model
    request.model_spec.signature_name = signature
    
    request.inputs['input'].CopyFrom(tf.contrib.util.make_tensor_proto(imgs, shape=imgs.shape))
    
    task_syncer.throttle()  ## concurrency control
    
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(1, task_syncer))

  #task_syncer.get_error_rate() ## wait !!
  task_syncer.wait_result() ## wait !!
  #print ("err#=", task_syncer._error)
  return task_syncer._fess


"""A GRPC client that talks to tensorflow_model_server loaded with FR model.

The client queries the service with face detected and cropped images to get the inference embeddings (face description vectors).

"""

class grpc_cli:

  def __init__(self):
    self.concurrency = 1   # maximum number of concurrent inference requests
    self.num_tests = 1   # Number of test images
    self.server = "frapi.ai.game.tw:8500" # PredictionService host:port
    self.work_dir = '/tmp' # Working directory
    self.model = "mnet1"
    self.signature = "mnet1_signature" # the same as fnet

  def img2fes(self, img):
    if (len(img.shape) == 3):
      imgs = img.reshape(1, 160, 160, 3)
    else:
      imgs = img
    return do_inference(self.server, self.work_dir, self.concurrency, self.num_tests, self.model, self.signature, imgs)

  def imgs2fess(self, imgs):
    n_imgs = imgs.shape[0]
    # todo: check n_imgs ...
    fess = do_inference(self.server, self.work_dir, self.concurrency, self.num_tests, self.model, self.signature, imgs)
    #print (fess.shape)
    return fess.reshape(n_imgs, 128)


    
    



