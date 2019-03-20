"""
WELDS section
"""
from .ordered_attrib import ET
from .base import DistItem, Section as InfotechSection, to_int
from . import reverse_orient


class Item(DistItem):
    """
    weld item from <WELDS> xml section
    <WLD
      IDTYPEOBJ="2097791" ODOMETER="0"
      NUM_TUBE="1" DL_TUBE="752" THICK="19.5" PSH1="11.6" PSH2="" REM=""
    />
    """
    xml_node_name = 'WLD'
    field_number = 'NUM_TUBE'
    field_length = 'DL_TUBE'
    field_thick = 'THICK'
    field_hor1 = 'PSH1'
    field_hor2 = 'PSH2'

    def __init__(self):
        super(Item, self).__init__()

        self.number = ''
        self.length = ''
        self.thick = ''
        self.hor1 = ''
        self.hor2 = ''

    @classmethod
    def from_xml(cls, xml_item):
        """
        create weld item from existing xml element
        """
        obj = cls()
        obj.fill_from_xml(xml_item)

        obj.number = xml_item.attrib[Item.field_number]
        obj.length = to_int(xml_item.attrib[Item.field_length])
        obj.thick = xml_item.attrib[Item.field_thick]
        obj.hor1 = xml_item.attrib[Item.field_hor1]
        obj.hor2 = xml_item.attrib[Item.field_hor2]

        return obj

    def end(self):
        """
        return distance for end of tube
        """
        return self.dist + self.length

    def as_csv_row(self, infotech, with_navigation=False):
        """
        return list of field values for csv string
        """
        columns = [
          self.number,
          "{}".format(self.length),
          self.thick.replace('.', ','),
          self.hor1.replace('.', ','),
          self.hor2.replace('.', ','),
        ]
        base_columns = super(Item, self).as_csv_row(infotech, with_navigation=with_navigation)

        return base_columns[:2] + columns + base_columns[2:]

    def reverse(self, total_length, object_index):
        """
        reverse weld
        """
        self.dist = total_length - (self.dist + self.length)
        self.number = "{}".format(object_index)
        self.hor1 = reverse_orient(self.hor1)
        self.hor2 = reverse_orient(self.hor2)

    def add_xml_child(self, parent_node):
        """
        create and add xmml node of weld to parent xml node
        """
        node = ET.SubElement(parent_node, Item.xml_node_name)
        super(Item, self).base_xml(node)
        node.set(Item.field_number, self.number)
        node.set(Item.field_length, "{}".format(self.length))
        node.set(Item.field_thick, self.thick)
        node.set(Item.field_hor1, self.hor1)
        node.set(Item.field_hor2, self.hor2)

        return node


class Section(InfotechSection):
    """
    <WELDS> xml section
    """
    item_attributes = DistItem.dist_attribs + [
      Item.field_number,
      Item.field_length,
      Item.field_thick,
      Item.field_hor1,
      Item.field_hor2,
      DistItem.field_comment,
    ] + DistItem.coords_attribs

    def __init__(self, infotech):
        super(Section, self).__init__(infotech, Item, 'WELDS')

    def as_csv(self, with_navigation=False):
        """
        dump weld section content as csv string
        """
        column_titles = [
          'Name', 'Distance', 'Tube number', 'Tube length', 'Thick', 'Weld1', 'Weld2', 'Comment'
        ]
        return super(Section, self).as_csv_body('Welds table', column_titles, with_navigation=with_navigation)

    def add_tube(self, objtype, tube_dist, tube_length):
        """
        add new tube with given type, dist and length to thr end of record
        """
        item = Item()

        item.objtype = objtype
        item.dist = tube_dist
        item.comment = ''

        item.number = ''
        item.length = tube_length
        item.thick = self.items[-1].thick
        item.hor1 = ''
        item.hor2 = ''

        self._items.append(item)
