from os.path import join
from skimage.transform import resize
from imageio import imread

import numpy as np
import chainer
from chainer.datasets import LabeledImageDataset
from chainer_addons.utils.imgproc import Augmentation


class PreprocessMixin(object):

	def __init__(self, size, preprocess=None, return_orig=False, *args, **kwargs):
		super(PreprocessMixin, self).__init__(*args, **kwargs)
		self._size = size if isinstance(size, tuple) else (size, size)
		self._preprocess = preprocess
		self.return_orig = return_orig

	@property
	def size(self):
		return self._size

	def preprocess(self, im):
		if self._preprocess is not None and callable(self._preprocess):
			return self._preprocess(im, size=self.size)
		else:
			return resize(im, self.size).transpose(2, 0, 1)

	def get_example(self, i):
		orig, lab = super(PreprocessMixin, self).get_example(i)
		if isinstance(orig, np.ndarray):
			if orig.ndim == 3:
				# single image is present
				im = self.preprocess(orig)
			elif orig.ndim == 4:
				# batch of images (parts)
				im = np.array([self.preprocess(im) for im in orig])
			else:
				raise ValueError("Incorrent input dimensions: {}!".format(orig.ndim))
		elif isinstance(orig, (list, tuple)):
			# batch of images (parts)
			im = np.array([self.preprocess(im) for im in orig])
		else:
			raise TypeError("Incorrent input type: {}!".format(type(orig)))

		if self.return_orig:
			return orig, im, lab
		else:
			return im, lab

class AugmentationMixin(object):

	def __init__(self, augment=None, *args, **kwargs):
		super(AugmentationMixin, self).__init__(*args, **kwargs)
		self._augment = augment

		self._augmentor = Augmentation()
		self._augmentor.random_crop(self._size).random_horizontal_flip()

	@property
	def augment(self):
		return self._augment and chainer.config.train

	def augmentor(self, im):
		if im.ndim == 3:
			# single image is present
			return self._augmentor(im)
		elif im.ndim == 4:
			# batch of images (parts)
			return np.array([self._augmentor(i) for i in im])
		else:
			raise ValueError("Incorrent input dimensions!")


	def get_example(self, i):
		res = super(AugmentationMixin, self).get_example(i)
		if not self.augment:
			return res

		if len(res) == 2:
			im, lab = res
			return self.augmentor(im), lab
		elif len(res) == 3:
			orig, im, lab = res
			return orig, self.augmentor(im), lab
		else:
			raise ValueError("Result was not expected!")

	@property
	def size(self):
		if self.augment:
			return tuple(int(s / .875) for s in self._size)
		else:
			return self._size

class ImageDataset(AugmentationMixin, PreprocessMixin, LabeledImageDataset):
	label_shift = 1

	@classmethod
	def create(cls, opts, data, images_folder="images", *args, **kw):
		return cls(size=opts.size,
			pairs=join(opts.root, data),
			root=join(opts.root, images_folder),
			*args, **kw)


