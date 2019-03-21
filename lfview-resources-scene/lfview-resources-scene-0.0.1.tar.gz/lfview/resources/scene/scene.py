"""Components required to construct a 3D scene with views of Element"""
from collections import OrderedDict

from lfview.resources import spatial
import properties
from properties.extras import Pointer


class _BaseSceneComponent(properties.HasProperties):
    """Base class for the Scene and all objects within a scene"""
    _REGISTRY = OrderedDict()

    uid = properties.String('Locally unique ID from client', required=False)


class Light(_BaseSceneComponent):
    """Light source for a scene"""
    direction = properties.Vector3(
        'Vector pointing from plot center to light',
    )
    brightness = properties.Float('Intensity of light source')
    enabled = properties.Boolean('Whether light is on or off')


class Slice(_BaseSceneComponent):
    """Position and color information for a slice in the Scene"""
    _defaults = {'uid': 'slice'}
    position_a = properties.Vector3(
        'Position of first plane',
        default=lambda: [0, 0, 0],
    )
    position_b = properties.Vector3(
        'Position of second plane; only required in section mode',
        default=[0, 0, 0],
        required=False,
    )
    normal = properties.Vector3(
        'Normal vector to the slice plane',
        default=lambda: [1., 0, 0],
    )
    mode = properties.StringChoice(
        'Slice mode',
        ['inactive', 'normal', 'reversed', 'section'],
        descriptions={
            'inactive': 'Slice is currently disabled',
            'normal': 'Standard single slice slicing mode',
            'reversed': 'Single slice with swapped normal',
            'section': 'Mode with two parallel sliceplanes'
        },
        default='inactive',
    )
    color_a = properties.Color(
        'Color of first slice',
        default=[0, 120, 255],
        serializer=spatial.mappings.to_hex,
        deserializer=spatial.mappings.from_hex,
    )
    color_b = properties.Color(
        'Color of second slice; only required in section mode',
        default=[253, 102, 0],
        required=False,
        serializer=spatial.mappings.to_hex,
        deserializer=spatial.mappings.from_hex,
    )

    @properties.validator
    def _validate_section(self):
        """Validate that position_b and color_b are set in section mode"""
        if (self.mode == 'section'
                and (self.position_b is None or self.color_b is None)):
            raise properties.ValidationError(
                message='Section mode requires position_b and color_b',
                reason='invalid',
                prop='mode',
                instance=self,
            )


class SliceGroup(_BaseSceneComponent):
    """Class describing a group of slices

    These slice the same views in the same style (union vs intersection)
    """
    _defaults = {'uid': 'slice_group'}
    slices = properties.List(
        'Slices in this group; only one is currently supported',
        Slice,
        min_length=1,
        max_length=1,
        default=lambda: [Slice()]
    )
    style = properties.StringChoice(
        'How slices in this group are combined',
        choices=[
            'union',
            'intersection',
        ],
        default='intersection',
    )


class Ruler(_BaseSceneComponent):
    """Ruler class

    Contains the path of the ruler as well as info
    about the objects it is measuring to and from
    """
    positions = properties.List(
        'Endpoints of the ruler',
        properties.Vector3(''),
        min_length=2,
        max_length=2,
    )
    objects = properties.List(
        'URL pointers of objects we are measuring from/to',
        Pointer('', spatial.elements._BaseElement),
        min_length=2,
        max_length=2,
    )


class _BaseCamera(_BaseSceneComponent):
    """Base Camera class from which all cameras must inherit"""


class CameraStandard(_BaseCamera):
    """Base class for Standard Cameras

    Both orthographic and perspective cameras are built on this
    """
    mode = properties.StringChoice(
        'View mode of camera',
        choices=['perspective', 'orthographic'],
        default='orthographic',
    )
    target = properties.Vector3(
        'Center of rotation of camera relative to the scene origin',
        default=lambda: [0., 0., 0.],
    )
    radius = properties.Float(
        'Distance of camera to target',
        default=5.,
    )
    zoom = properties.Float(
        'Zoom level of camera',
        default=1.,
    )
    rotation = properties.List(
        'Quaternion rotation of the camera relative to the scene',
        properties.Float(''),
        min_length=4,
        max_length=4,
        default=lambda: [0., 0., 0., 1.],
    )
    up_direction = properties.Vector3(
        'Up direction of camera',
        default='up',
    )


class _BaseElementView(_BaseSceneComponent):
    """Base View class for all views to inherit from

    Contains basic meta properties (color, opacity, visible)
    and supports data mapping to the opacity and color attributes
    """
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.elements._BaseElement,
    )
    slice_group = properties.String(
        'Local SliceGroup UID from the plot which slices this view',
        default='slice_group',
        required=False,
    )


class PointSet(_BaseElementView, spatial.OptionsPoints):
    """PointSetView class, used by PointSet Element

    Supports data mapping to the point size attribute
    """
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementPointSet,
    )


class Lines(_BaseElementView, spatial.OptionsLines):
    """LineSetView class, used by LineSet Element"""
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementLineSet,
    )


class Tubes(_BaseElementView, spatial.OptionsTubes):
    """TubesView class, used by LineSet Element

    Supports data mapping to the radius attribute
    """
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementLineSet,
    )


class Surface(_BaseElementView, spatial.OptionsSurface):
    """SurfaceView class, used by SurfaceElement"""
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementSurface,
    )


class SurfaceGrid(Surface):
    """SurfaceGridView class, used by element with SurfaceGrid geometry"""
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementSurfaceGrid,
    )


class BlockModel(_BaseElementView, spatial.OptionsBlockModel):
    """BlockModelView class, used by Volume Element"""
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementVolumeGrid,
    )


class VolumeSlices(_BaseElementView, spatial.OptionsVolumeSlices):
    """VolumeSlicesView class, used by Volume Element"""
    element = Pointer(
        'URL pointer of element associated with this view',
        spatial.ElementVolumeGrid,
    )


class Plot(_BaseSceneComponent):
    """Object describing the contents of the 3D scene

    Contains info about how a plot is positioned in the scene, as well
    as the plot limits. Also contains active elements, slices, and
    measurements in the plot.
    """
    position = properties.Vector3(
        'x,y,z position of the plot center relative to scene origin',
        default=lambda: [0., 0, 0],
    )
    scale = properties.Vector3(
        'x,y,z scale of the plot coordinate system relative to scene '
        'coordinate system',
        default=lambda: [1., 1, 1],
    )
    rotation = properties.List(
        'Quaternion rotation of plot axes relative to scene axes',
        properties.Float(''),
        min_length=4,
        max_length=4,
        default=lambda: [0., 0, 0, 1],
    )
    lims = properties.List(
        'x,y,z limits, defined in plot coordinates',
        properties.Vector2(''),
        min_length=3,
        max_length=3,
        default=lambda: [[0, 0.00001]] * 3,
    )
    exaggeration = properties.List(
        'x,y,z exaggeration of the plot coordinates',
        properties.Integer('', min=1),
        default=lambda: [1, 1, 1],
    )
    slice_groups = properties.List(
        'Active slice groups; currently only one is supported',
        SliceGroup,
        max_length=1,
        default=lambda: [SliceGroup()],
    )
    measurements = properties.List(
        'List of active ruler instances; currently only one is supported',
        Ruler,
        max_length=1,
        default=list,
    )
    views = properties.List(
        'List of element views in the plot',
        properties.Union(
            '', [
                view for key, view in _BaseSceneComponent._REGISTRY.items()
                if key[0] != '_' and issubclass(view, _BaseElementView)
            ]
        ),
        max_length=100,
        default=list,
    )


class Scene(_BaseSceneComponent):
    """State of the 3D scene

    Includes camera, lighting, and plot info
    """

    camera = properties.Instance(
        'Scene camera',
        CameraStandard,
        default=CameraStandard,
    )
    plots = properties.List(
        'Plots in the scene; currently only one is supported',
        Plot,
        max_length=1,
        default=lambda: [Plot()]
    )
    lights = properties.List(
        'Active lights',
        Light,
        max_length=4,
        default=list,
    )
