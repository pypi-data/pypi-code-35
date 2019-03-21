"""Slide object holding scene info and annotations"""
from collections import OrderedDict

from lfview.resources import files, spatial
import properties

from .scene import Scene


class _BaseSlideComponent(properties.HasProperties):
    """Base class for all slide components"""
    _REGISTRY = OrderedDict()


class _BaseAnnotation(_BaseSlideComponent):
    """Base class for all annotations"""
    uid = properties.String('Locally unique ID from client', required=False)
    position = properties.List(
        'Location of annotation on slide plane',
        properties.Float(''),
        min_length=2,
        max_length=2,
    )
    color = properties.Color('Annotation color')


class AnnotationText(_BaseAnnotation):
    """Text comment at a position on a slide"""
    comment = spatial.base.ShortString('Text comment', max_length=5000)


class AnnotationInk(_BaseAnnotation):
    """Pen-drawn annotation on a slide"""
    path = properties.List(
        'Ink path vertices, relative to position',
        properties.List('', properties.Float(''), min_length=2, max_length=2),
        max_length=2000,
    )


class DrawingPlane(_BaseSlideComponent):
    """2D drawing plane of the slide"""
    origin = properties.Vector3('Origin of drawing plane')
    axis_u = properties.Vector3('Horizontal axis of drawing plane')
    axis_v = properties.Vector3('Vertical axis of drawing plane')


class _BaseCollaborationModel(files.base._BaseUIDModel):
    """Base class for collaboration objects exposed in the API"""
    _REGISTRY = OrderedDict()


class Slide(_BaseCollaborationModel, spatial.base._BaseResource):
    """Slides provide a snapshot of a 3D scene

    They also provide a canvas for annotating the scene. By creating
    several slides, you can tell a story around your 3D data.
    """
    BASE_TYPE = 'slides'

    scene = spatial.base.InstanceSnapshot(
        'Current state of the 3D scene',
        instance_class=Scene,
    )
    annotation_plane = spatial.base.InstanceSnapshot(
        'Drawing plane for annotations perpendicular to line of sight',
        instance_class=DrawingPlane,
    )
    annotations = properties.List(
        'List of annotations on the scene',
        properties.Union(
            '',
            props=[
                spatial.base.InstanceSnapshot('', AnnotationText),
                spatial.base.InstanceSnapshot('', AnnotationInk),
            ],
        ),
        max_length=30,
        default=list,
    )


class Feedback(_BaseCollaborationModel):
    """Feedback allow others to respond slides and other feedback

    For now, these are only text comments.
    """
    BASE_TYPE = 'feedback'

    comment = spatial.base.ShortString(
        'A comment in response to a slide',
        max_length=5000,
    )
