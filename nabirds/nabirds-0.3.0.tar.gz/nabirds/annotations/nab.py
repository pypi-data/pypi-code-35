from os.path import join

from nabirds.utils import _MetaInfo
from .base import BaseAnnotations


class NAB_Annotations(BaseAnnotations):
	name="NABirds"

	@property
	def meta(self):
		info = _MetaInfo(
			images_folder="images",
			images_file="images.txt",
			labels_file="labels.txt",
			hierarchy_file="hierarchy.txt",
			split_file="train_test_split.txt",
			parts_file=join("parts", "part_locs.txt"),
			part_names_file=join("parts", "parts.txt"),
		)

		info.structure = [
			[info.images_file, "_images"],
			[info.labels_file, "labels"],
			[info.hierarchy_file, "hierarchy"],
			[info.split_file, "_split"],
			[info.parts_file, "_part_locs"],
			[info.part_names_file, "_part_names"],
		]
		return info
