import numpy as np

from os.path import join

from nabirds.utils import _MetaInfo
from .base import BaseAnnotations


class CARS_Annotations(BaseAnnotations):
	name="CARS"

	@property
	def meta(self):
		info = _MetaInfo(
			images_folder="images",
			images_file="images.txt",
			labels_file="labels.txt",
			split_file="tr_ID.txt",
			bounding_boxes="bounding_boxes.txt",
			bounding_box_dtype=np.dtype([(v, np.int32) for v in "xywh"]),
		)

		info.structure = [
			[info.images_file, "_images"],
			[info.labels_file, "labels"],
			[info.split_file, "_split"],
			[info.bounding_boxes, "_bounding_boxes"],
		]
		return info

	def __init__(self, *args, **kwargs):
		super(CARS_Annotations, self).__init__(*args, **kwargs)
		# set labels from [1..N] to [0..N-1]
		self.labels -= 1

	def _load_split(self):
		assert self._split is not None, "Train-test split was not loaded!"
		uuid_to_split = {uuid: int(split) for uuid, split in zip(self.uuids, self._split)}
		self.train_split = np.array([uuid_to_split[uuid] for uuid in self.uuids], dtype=bool)
		self.test_split = np.logical_not(self.train_split)

	def _load_parts(self):
		self.part_names = {}
		self._load_bounding_boxes()

	def _load_bounding_boxes(self):
		assert self._bounding_boxes is not None, "Bouding boxes were not loaded!"

		uuid_to_bbox = {}
		for content in [i.split() for i in self._bounding_boxes]:
			uuid, bbox = content[0], content[1:]
			uuid_to_bbox[uuid] = [float(i) for i in bbox]

		self.bounding_boxes = np.array(
			[tuple(uuid_to_bbox[uuid]) for uuid in self.uuids],
			dtype=self.meta.bounding_box_dtype)

	def parts(self, *args, **kwargs):
		return None

	def bounding_box(self, uuid):
		return self.bounding_boxes[self.uuid_to_idx[uuid]].copy()
