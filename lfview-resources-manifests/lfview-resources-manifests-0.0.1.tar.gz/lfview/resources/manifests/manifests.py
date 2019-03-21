"""Manifest resources that hold a list of other resources"""
from collections import OrderedDict

from lfview.resources import files, spatial
import properties
from properties.extras import Pointer


class _BaseManifest(spatial.base._BaseResource):  #pylint: disable=protected-access
    """Base class for Manifest resources

    Fundamentally, Manifests are defined by their contents, which is just
    a list of other resources. Manifests grant access to these other
    resources, so by sharing a Manifest you are also sharing the contents.
    """
    _REGISTRY = OrderedDict()

    contents = properties.List(
        'The resources contained in this manifest; access to a manifest '
        'grants access to the resources listed in its contents',
        prop=Pointer('Pointer to a item', files.base._BaseUIDModel),
        default=list,
    )


class ViewMetadata(spatial.base._BaseResource):
    """Metadata on View Manifests

    This gives the View more meaning outside of simply the contents
    to provide context on visualization.
    """

    label_x = spatial.base.ShortString(
        'X-axis label',
        max_length=300,
        required=False,
    )
    label_y = spatial.base.ShortString(
        'Y-axis label',
        max_length=300,
        required=False,
    )
    label_z = spatial.base.ShortString(
        'Z-axis label',
        max_length=300,
        required=False,
    )


class View(ViewMetadata, _BaseManifest):
    """Manifest class for visualizing Elements

    Like all Manifests, Views grant access to their contents. Views are
    also used for visualizing data by highlighting the important Elements
    and including some visualization metadata.

    In order for the View to grant access to certain elements, they must
    be specified in the contents list in addition to
    """
    BASE_TYPE = 'views'

    elements = properties.List(
        'A list of pointers to the elements in the View',
        prop=Pointer('Pointer to an element', spatial.elements._BaseElement),
        default=list,
        max_length=100,
    )
