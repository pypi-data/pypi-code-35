import numpy as np
import simplejson as json

from os.path import join

from nabirds.utils import _MetaInfo

from .base import BaseAnnotations

class INAT19_Annotations(BaseAnnotations):

	name="INAT19"

	@property
	def meta(self):
		info = _MetaInfo(
			images_folder="",
			content="trainval2019.json",
			val_content="val2019.json",
			# train_content="train2019.json",

			# fake bounding boxes: the whole image
			bounding_box_dtype=np.dtype([(v, np.int32) for v in "xywh"])
		)

		info.structure = [
			[info.content, "_content"],
			[info.val_content, "_val_content"],
		]
		return info

	def read_content(self, json_file, attr):
		with self._open(json_file) as f:
			content = json.load(f)
			setattr(self, attr, content)

	def parts(self, uuids):
		return None

	def bounding_box(self, uuid):
		return self.bounding_boxes[self.uuid_to_idx[uuid]].copy()

	def _load_bounding_boxes(self):
		self.bounding_boxes = np.zeros(len(self.uuids), dtype=self.meta.bounding_box_dtype)

		for i, im in enumerate(self._content["images"]):
			self.bounding_boxes[i]["w"] = im["width"]
			self.bounding_boxes[i]["h"] = im["height"]

	def _load_parts(self):
		self.part_names = {}
		self._load_bounding_boxes()

	def _load_split(self):
		self.train_split = np.ones(len(self.uuids), dtype=bool)
		val_uuids = [im["id"] for im in self._val_content["images"]]
		for v_uuid in val_uuids:
			self.train_split[self.uuid_to_idx[v_uuid]] = False

		self.test_split = np.logical_not(self.train_split)

	def _load_labels(self):
		self.labels = np.zeros(len(self.uuids), dtype=np.int32)
		labs = {annot["image_id"]: annot["category_id"] for annot in self._content["annotations"]}
		for uuid in self.uuids:
			self.labels[self.uuid_to_idx[uuid]] = labs[uuid]

	def _load_uuids(self):
		uuid_fnames = [(im["id"], im["file_name"]) for im in self._content["images"]]
		self.uuids, self.images = map(np.array, zip(*uuid_fnames))
		self.uuid_to_idx = {uuid: i for i, uuid in enumerate(self.uuids)}
