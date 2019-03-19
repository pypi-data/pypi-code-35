from .cub import CUB_Annotations
from .nab import NAB_Annotations

from cvargparse.utils import BaseChoiceType

class AnnotationType(BaseChoiceType):
	NAB = NAB_Annotations
	CUB = CUB_Annotations

	Default = CUB
