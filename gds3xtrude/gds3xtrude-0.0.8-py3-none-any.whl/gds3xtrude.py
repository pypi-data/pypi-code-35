##
## Copyright (c) 2018-2019 Thomas Kramer.
## 
## This file is part of gds3xtrude 
## (see https://codeberg.org/tok/gds3xtrude).
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
## 
## You should have received a copy of the GNU Affero General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##

from .polygon_approx import approximate_polygon
from .layer_operations import LayerOp, AbstractLayer

from functools import reduce
from itertools import chain
import importlib.util
import importlib.machinery
import types
import logging

from typing import Dict, List, Tuple, Optional

from .builder import LayerStackBuilder, ApproximateLayerStackBuilder
from .types import Material

logger = logging.getLogger(__name__)

# klayout.db should not be imported if script is run from KLayout GUI.
try:
    import pya
except:
    import klayout.db as pya

DEFAULT_COLOR = [0.5, 0.5, 0.5]
DEFAULT_MATERIAL = Material('DEFAULT_MATERIAL', color=DEFAULT_COLOR)


class Mask:
    """ Wrapper around pya.Region.
    """

    def __init__(self, region: pya.Region):
        self.region = region
        self.material = Material('<unnamed>', color=DEFAULT_COLOR)

    def __add__(self, other):
        return Mask(self.region + other.region)

    def __or__(self, other):
        return self + other

    def __and__(self, other):
        return Mask(self.region & other.region)

    def __sub__(self, other):
        m = Mask(self.region - other.region)
        m.material = self.material
        return m

    def __xor__(self, other):
        return Mask(self.region ^ other.region)

    def __hash__(self):
        return hash(self.region)

    def __equal__(self, other):
        return self.region == other.region


def _build_masks(layout: pya.Layout,
                 cell: pya.Cell,
                 abstract_layerstack: List[Tuple[int, List[AbstractLayer]]],
                 selection_box: Optional[pya.Box] = None,
                 material_map: Optional[Dict[Tuple[int, int], Material]] = None,
                 default_material: Material = DEFAULT_MATERIAL) -> List[Tuple[int, List[pya.Region]]]:
    """ Create the masks of `cell` based on the layer stack information.
    :param layout:
    :param cell:
    :param abstract_layerstack: Layer stack structure as defined in the technology file.
    :param selection_box: An optional pya.Box to select which part of the layout should be converted to masks.
    :param material_map:   Mapping from layer number to color. Dict[(int, int), (r, g, b)]
    :param default_material: Color to be used if it is not defined in `color_map`. (r, g, b), 0 <= r, g, b <= 1
    :return: List[(thickness: int, mask: pya.Region)]
    """

    # Cache for evaluated sub trees.
    cache = dict()

    def eval_op_tree(op_node):
        """ Recursively evaluate the layer operation tree.
        :param op_node: Operand node or leaf.
        :return: Returns a `Mask` object containing a `pya.Region` of the layer.
        """

        if op_node in cache:
            return cache[op_node]

        if isinstance(op_node, AbstractLayer):
            (idx, purpose, material) = op_node.eval()
            layer_index = layout.layer(idx, purpose)

            region = _flatten_cell(cell, layer_index, selection_box=selection_box)
            if selection_box is not None:
                region = region & selection_box

            result = Mask(region)
            if material_map is not None:
                result.material = material_map.get((idx, purpose), default_material)
            else:
                result.material = material if material is not None else default_material
        else:
            assert isinstance(op_node, LayerOp)
            op = op_node.op
            lhs = eval_op_tree(op_node.lhs)
            rhs = eval_op_tree(op_node.rhs)
            result = op(lhs, rhs)
        result.region.merge()
        cache[op_node] = result

        return result

    _layerstack = []
    for thickness, layers in abstract_layerstack:
        if not isinstance(layers, list):
            layers = [layers]

        _layerstack.append(
            (thickness, [eval_op_tree(l) for l in layers])
        )

    return _layerstack


def _flatten_cell(cell: pya.Cell, layer_index: int,
                  selection_box: Optional[pya.Box] = None,
                  cell_cache: Optional[Dict[int, pya.Region]] = None) -> pya.Region:
    """ Recursively convert a single layer of a cell into a pya.Region.
    :param cell: The pya.Cell to be converted.
    :param layer_index: KLayout layer index.
    :param cell_cache: Dict mapping cell indices to flattened `pya.Region`s. This allows to reuse flattened cells.
    :return: Merged pya.Region containing all polygons of the flattened cell hierarchy.
    """

    if cell_cache is None:
        # Cache rendered cells
        # Dict[cell_index, volume]
        cell_cache = dict()

    region = pya.Region()

    if selection_box is None:
        instances = cell.each_inst()
    else:
        instances = cell.each_touching_inst(selection_box)

    for inst in instances:
        cell_id = inst.cell_index
        trans = inst.cplx_trans

        # Transform selection such that it can be used in recursive call.
        if selection_box:
            trans_selection = selection_box.transformed(trans.inverted())
        else:
            trans_selection = None

        if cell_id in cell_cache:
            child_region = cell_cache[cell_id]
            if trans_selection is not None:
                child_region = child_region & trans_selection
        else:
            # Recursively flatten child instance.
            child_region = _flatten_cell(inst.cell, layer_index,
                                         selection_box=trans_selection, cell_cache=cell_cache)

            # Cache the region only if the cell has been fully rendered and was not cropped to selection.
            if trans_selection is None or inst.cell.bbox().inside(trans_selection):
                cell_cache[cell_id] = child_region

        transformed = child_region.transformed(trans)
        region.insert(transformed)

    # Add shapes of this cell.

    if selection_box is None:
        own_shapes = cell.each_shape(layer_index)
    else:
        own_shapes = cell.each_touching_shape(layer_index, selection_box)

    # region.insert(own_shapes)
    for shape in own_shapes:
        polygon = shape.polygon
        # Texts may have no polygon representation.
        if polygon is not None:
            region.insert(shape.polygon)

    region.merge()
    return region


def build_layerstack(builder: LayerStackBuilder,
                     layout: pya.Layout,
                     top_cell: pya.Cell,
                     tech_file,
                     approx_error: float = 0,
                     material_map: Optional[Dict[Tuple[int, int], Material]] = None,
                     centered: bool = False,
                     scale_factor: float = 1,
                     selection_box: Optional[pya.Box] = None):
    """ Transform the first pya.Cell in `layout` into a solidpython volume.
    :param layout:  pya.Layout
    :param top_cell: pya.Cell
    :param tech_file:   Path to description of the layer stack.
    :param approx_error:    Approximate polygons before conversion.
    :param material_map:   Mapping from layer number to color. Dict[(int, int), (r, g, b)]
    :param centered:    Move the center of the layout to (0, 0).
    :param scale_factor:    Scale the layout before conversion.
    :param selection_box: An optional pya.Box to select which part of the layout should be converted to masks.
    :return: solidpython volume
    """

    logger.info('Loading tech file: %s', tech_file)

    loader = importlib.machinery.SourceFileLoader('tech', tech_file)
    tech = types.ModuleType(loader.name)
    loader.exec_module(tech)

    logger.info("Convert polygons into volumes.")

    layer_masks = _build_masks(layout, top_cell, tech.layerstack, material_map=material_map, selection_box=selection_box)

    approx_builder = ApproximateLayerStackBuilder(builder, approx_error=approx_error)

    offset = 0
    for thickness, masks in layer_masks:
        for mask in masks:
            approx_builder.add_region(mask.region, thickness=thickness, z_offset=offset, material=mask.material)

        offset += thickness

    # Find bounding box of masks and center the volume.
    if centered and len(layer_masks) > 0:
        bboxes = chain(*((mask.region.bbox() for mask in masks) for (thickness, masks) in layer_masks))
        # Find union bounding box.
        bbox = reduce(lambda a, b: a + b, bboxes)
        # Shift center to (0, 0).
        center = bbox.center()
        builder.translate((-center.x, -center.y, 0))

    if scale_factor != 1:
        builder.scale(scale_factor)
