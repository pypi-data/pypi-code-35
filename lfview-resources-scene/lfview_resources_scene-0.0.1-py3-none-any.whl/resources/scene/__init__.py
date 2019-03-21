from . import scene, slide
from .scene import (
    Light,
    Slice,
    SliceGroup,
    Ruler,
    CameraStandard,
    PointSet,
    Lines,
    Tubes,
    Surface,
    SurfaceGrid,
    BlockModel,
    VolumeSlices,
    Plot,
    Scene,
)
from .slide import (
    Feedback,
    Slide,
    AnnotationInk,
    AnnotationText,
    DrawingPlane,
)

__version__ = '0.0.1'

SCENE_REGISTRY = slide._BaseCollaborationModel._REGISTRY
