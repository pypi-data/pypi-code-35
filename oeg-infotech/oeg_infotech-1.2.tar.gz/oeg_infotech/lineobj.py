"""
LINEOBJS section
"""
from .ordered_attrib import ET
from .base import Section as InfotechSection, DistItem
from .codes import Feature


REVERTED = {
  Feature.WATER_START: Feature.WATER_END,
  Feature.WATER_END: Feature.WATER_START,

  Feature.METALL_CASE_START: Feature.METALL_CASE_END,
  Feature.METALL_CASE_END: Feature.METALL_CASE_START,

  Feature.KOMPOS_CASE_START: Feature.KOMPOS_CASE_END,
  Feature.KOMPOS_CASE_END: Feature.KOMPOS_CASE_START,

  Feature.CASE_START: Feature.CASE_END,
  Feature.CASE_END: Feature.CASE_START,

  Feature.PRIGRUZ_START: Feature.PRIGRUZ_END,
  Feature.PRIGRUZ_END: Feature.PRIGRUZ_START,

  Feature.TURN_START: Feature.TURN_END,
  Feature.TURN_END: Feature.TURN_START,

  Feature.TURN_SEGM_START: Feature.TURN_SEGM_END,
  Feature.TURN_SEGM_END: Feature.TURN_SEGM_START,
}


class Item(DistItem):
    """
    object item from <LINEOBJS> xml section
    <PLOBJ
      IDTYPEOBJ="990006537229" ODOMETER="0" NAME_MARKER="M1" L_LCH="" REM=""
    />
    """
    xml_node_name = 'PLOBJ'
    field_name_marker = 'NAME_MARKER'
    field_piketag_km = 'L_LCH'

    def __init__(self):
        super(Item, self).__init__()
        self.marker_name = ''
        self.piketag_km = ''

    @classmethod
    def from_xml(cls, xml_item):
        """
        create lineobj item from existing xml element
        """
        obj = cls()
        obj.fill_from_xml(xml_item)

        obj.marker_name = xml_item.attrib[Item.field_name_marker]
        obj.piketag_km = xml_item.attrib[Item.field_piketag_km]

        return obj

    def as_csv_row(self, infotech, with_navigation=False):
        """
        return list of lineobj field values for csv string
        """
        columns = [self.marker_name, self.piketag_km]
        base_columns = super(Item, self).as_csv_row(infotech, with_navigation=with_navigation)

        return base_columns[:2] + columns + base_columns[2:]

    def add_xml_child(self, parent_node):
        """
        create and add lineobj xml node of object to parent xml node
        """
        node = ET.SubElement(parent_node, Item.xml_node_name)
        super(Item, self).base_xml(node)
        node.set(Item.field_name_marker, self.marker_name)
        node.set(Item.field_piketag_km, self.piketag_km)

        return node

    def reverse(self, total_length, object_index):
        """
        reverse line object
        """
        super(Item, self).reverse(total_length, object_index)
        if self.objtype in REVERTED:
            self.objtype = REVERTED[self.objtype]


class Section(InfotechSection):
    """
    <LINEOBJS> xml section
    """
    section_tag = 'LINEOBJS'

    item_attributes = DistItem.dist_attribs + [
      Item.field_name_marker,
      Item.field_piketag_km,
      DistItem.field_comment,
    ] + DistItem.coords_attribs

    def __init__(self, infotech):
        super(Section, self).__init__(infotech, Item, Section.section_tag)

    def as_csv(self, with_navigation=False):
        """
        dump lineobj section content as csv string
        """
        column_titles = [
          'Name', 'Distance', 'Marker', 'Piketag', 'Comment'
        ]
        return super(Section, self).as_csv_body('Line objects table', column_titles, with_navigation=with_navigation)
