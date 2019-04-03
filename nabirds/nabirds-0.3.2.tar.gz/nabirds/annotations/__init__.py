from .cub import CUB_Annotations
from .nab import NAB_Annotations
from .cars import CARS_Annotations
from .inat import INAT19_Annotations

from cvargparse.utils import BaseChoiceType

class AnnotationType(BaseChoiceType):
	CUB200 = CUB_Annotations
	NAB = NAB_Annotations
	CARS = CARS_Annotations
	INAT19 = INAT19_Annotations

	Default = CUB200
