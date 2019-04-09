import os
from subprocess import call
from functools import partial
from .binary_wrapper import BinaryWrapper

def ensure_list(val):
  if isinstance(val, (tuple, list)):
    return list(val)
  else:
    return [val]

class TerminalPlot():
  file_name = 'plot.png'

  def __init__(self, plt):
    with BinaryWrapper() as binary_wrapper:
      plt.savefig(binary_wrapper.path / self.file_name)
      plt.close()
      self.binary_wrapper = binary_wrapper

  def show(self):
    with self.binary_wrapper.unwrap() as path:
      call(['imgcat', path / self.file_name])

  def savefig(self, target_path):
    with self.binary_wrapper.unwrap() as path:
      os.rename(path / self.file_name, target_path)

class PickleableKerasModel():
  file_name = 'model.h5'

  def __init__(self, model):
    with BinaryWrapper() as binary_wrapper:
      model.save(binary_wrapper.path / self.file_name)
      self.binary_wrapper = binary_wrapper

  def unwrap(self):
    from keras.models import load_model
    with self.binary_wrapper.unwrap() as path:
      return load_model(path / self.file_name)

class PickleableTf:
  def __init__(self, get_model_funcs, *args, **kwargs):
    from checkpointer import get_function_hash

    model_funcs_names = kwargs.get('model_funcs_names', None)
    binary_wrapper = kwargs.get('binary_wrapper', None)

    if 'model_funcs_names' in kwargs:
      del kwargs['model_funcs_names']
      del kwargs['binary_wrapper']

    if model_funcs_names == None:
      import tensorflow as tf

      with tf.Graph().as_default():
        model_funcs = ensure_list(get_model_funcs(*args, **kwargs))
        model_funcs_names = [func.__name__ for func in model_funcs]

    self.args = args
    self.kwargs = kwargs
    self.model_funcs_names = model_funcs_names
    self.get_model_funcs = get_model_funcs
    self.get_model_funcs_hash = get_function_hash(get_model_funcs)
    self.binary_wrapper = binary_wrapper

    for func_name in model_funcs_names:
      compute = partial(self._compute, func_name)
      setattr(self, func_name, compute)

  def _compute(self, func_name, *args, **kwargs):
    import tensorflow as tf

    with tf.Graph().as_default():
      model_funcs = {
        func.__name__: func
        for func in ensure_list(self.get_model_funcs(*self.args, **self.kwargs))
      }

      ckpt_file_name = 'tf.ckpt'
      saver = tf.train.Saver()

      with tf.Session() as sess:
        binary_wrapper = self.binary_wrapper

        def save():
          nonlocal binary_wrapper
          with BinaryWrapper() as binary_wrapper:
            saver.save(sess, binary_wrapper.path / ckpt_file_name)

        if self.binary_wrapper:
          with self.binary_wrapper.unwrap() as path:
            saver.restore(sess, path / ckpt_file_name)
        else:
          init_op = tf.global_variables_initializer()
          sess.run(init_op)

        result = model_funcs[func_name](sess, save, *args, **kwargs)
        model = PickleableTf(
          self.get_model_funcs,
          *self.args,
          **self.kwargs,
          model_funcs_names=self.model_funcs_names,
          binary_wrapper=binary_wrapper
        )
        return model, result
