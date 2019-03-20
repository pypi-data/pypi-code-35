"""
DEFECTS section
"""
from .ordered_attrib import ET
from .base import Section as InfotechSection, DistItem, to_int
from . import reverse_orient


class Item(DistItem):  # pylint: disable=too-many-instance-attributes
    """
    defect item from <DEFECTS> xml section
    <DEF
      IDTYPEOBJ="990004698869" ODOMETER="145"
      L_OTCH="170" W_OTCH="309" V_MIN_OTCH="5" V_MAX_OTCH="5" ORIENT1="7.2" ORIENT2="8.1" NUMDEF="2" REM=""
      KBD="0.70" PBEZ="" TIME_LIMIT="23.686" PBEZ_PERCENT="" METHOD="6907370"
    />
    """
    xml_node_name = 'DEF'
    field_length = 'L_OTCH'
    field_width = 'W_OTCH'
    field_loss_min = 'V_MIN_OTCH'
    field_loss_max = 'V_MAX_OTCH'
    field_orient_start = 'ORIENT1'
    field_orient_end = 'ORIENT2'
    field_number = 'NUMDEF'
    field_kbd = 'KBD'
    field_safe_pressure = 'PBEZ'
    field_time_limit = 'TIME_LIMIT'
    field_safe_pressure_persent = 'PBEZ_PERCENT'
    field_method_id = 'METHOD'

    def __init__(self):
        super(Item, self).__init__()

        self.length = ''
        self.width = ''
        self.loss_min = ''
        self.loss_max = ''
        self.orient_start = ''
        self.orient_end = ''
        self.number = ''
        self.kbd = ''
        self.safe_pressure = ''
        self.time_limit = ''
        self.safe_pressure_persent = ''
        self.method_id = ''

    @classmethod
    def from_xml(cls, xml_item):
        """
        create defect item from existing xml element
        """
        obj = cls()
        obj.fill_from_xml(xml_item)

        obj.length = to_int(xml_item.attrib[Item.field_length])  # mm
        obj.width = to_int(xml_item.attrib[Item.field_width])  # mm
        obj.loss_min = to_int(xml_item.attrib[Item.field_loss_min])  # % or mm
        obj.loss_max = to_int(xml_item.attrib[Item.field_loss_max])  # % or mm
        obj.orient_start = xml_item.attrib[Item.field_orient_start]  # hour
        obj.orient_end = xml_item.attrib[Item.field_orient_end]  # hour
        obj.number = xml_item.attrib[Item.field_number]
        obj.kbd = xml_item.attrib[Item.field_kbd]
        obj.safe_pressure = xml_item.attrib[Item.field_safe_pressure]
        obj.time_limit = xml_item.attrib[Item.field_time_limit]
        obj.safe_pressure_persent = xml_item.attrib[Item.field_safe_pressure_persent]
        obj.method_id = xml_item.attrib[Item.field_method_id]

        return obj

    def as_csv_row(self, infotech, with_navigation=False):
        """
        return list of defect field values for csv string
        """
        method = ''
        if self.method_id in infotech.obj_dict:
            method = infotech.obj_dict[self.method_id]

        columns = [
          "{}".format(self.length),
          "{}".format(self.width),
          "{}".format(self.loss_min),
          "{}".format(self.loss_max),
          self.orient_start.replace('.', ','),
          self.orient_end.replace('.', ','),
          self.kbd,
          self.safe_pressure,
          self.time_limit,
          self.safe_pressure_persent,
          method,
        ]
        base_columns = super(Item, self).as_csv_row(infotech, with_navigation=with_navigation)

        return [self.number] + base_columns[:2] + columns + base_columns[2:]

    def reverse(self, total_length, object_index):
        """
        reverse defect
        """
        self.dist = total_length - self.dist
        if self.length:
            self.dist -= int(self.length / 10)

        self.number = "{}".format(object_index)
        self.orient_start = reverse_orient(self.orient_start)
        self.orient_end = reverse_orient(self.orient_end)

    def add_xml_child(self, parent_node):
        """
        create and add xmml node of defect to parent xml node
        """
        node = ET.SubElement(parent_node, Item.xml_node_name)
        super(Item, self).base_xml(node)
        node.set(Item.field_length, "{}".format(self.length))
        node.set(Item.field_width, "{}".format(self.width))
        node.set(Item.field_loss_min, "{}".format(self.loss_min))
        node.set(Item.field_loss_max, "{}".format(self.loss_max))
        node.set(Item.field_orient_start, self.orient_start)
        node.set(Item.field_orient_end, self.orient_end)
        node.set(Item.field_number, self.number)
        node.set(Item.field_kbd, self.kbd)
        node.set(Item.field_safe_pressure, self.safe_pressure)
        node.set(Item.field_time_limit, self.time_limit)
        node.set(Item.field_safe_pressure_persent, self.safe_pressure_persent)
        node.set(Item.field_method_id, self.method_id)

        return node


class Section(InfotechSection):
    """
    <DEFECTS> xml section
    """
    item_attributes = DistItem.dist_attribs + [
      Item.field_length,
      Item.field_width,
      Item.field_loss_min,
      Item.field_loss_max,
      Item.field_orient_start,
      Item.field_orient_end,
      Item.field_number,
      DistItem.field_comment,
      Item.field_kbd,
      Item.field_safe_pressure,
      Item.field_time_limit,
      Item.field_safe_pressure_persent,
      Item.field_method_id,
    ] + DistItem.coords_attribs

    def __init__(self, infotech):
        super(Section, self).__init__(infotech, Item, 'DEFECTS')

    def as_csv(self, with_navigation=False):
        """
        dump defects section content as csv string
        """
        column_titles = [
          'Number',
          'Name', 'Distance',
          'Length', 'Width', 'Loss min', 'Loss max', 'Orient start', 'Orient end',
          'KBD', 'Safe pressure', 'Time limit', 'Press percent', 'Method',
          'Comment',
        ]
        return super(Section, self).as_csv_body('Defects table', column_titles, with_navigation=with_navigation)

    def danger_stats(self):
        """
        generate statistics about defects danger data
        """
        stats_values = {
          DistItem.field_typeobj: [],
          Item.field_method_id: [],
        }
        stats_counts = {
          Item.field_kbd: 0,
          Item.field_safe_pressure: 0,
          Item.field_time_limit: 0,
          Item.field_safe_pressure_persent: 0,
          Item.field_method_id: 0,
        }

        for item in self.items:
            is_kbd = False

            if item.kbd:
                stats_counts[Item.field_kbd] += 1
                is_kbd = True

            if item.safe_pressure:
                stats_counts[Item.field_safe_pressure] += 1
                is_kbd = True

            if item.time_limit:
                stats_counts[Item.field_time_limit] += 1
                is_kbd = True

            if item.safe_pressure_persent:
                stats_counts[Item.field_safe_pressure_persent] += 1
                is_kbd = True

            if item.method_id:
                stats_counts[Item.field_method_id] += 1
                is_kbd = True
                if item.method_id not in stats_values[Item.field_method_id]:
                    stats_values[Item.field_method_id].append(item.method_id)

            if is_kbd:
                if item.objtype not in stats_values[DistItem.field_typeobj]:
                    stats_values[DistItem.field_typeobj].append(item.objtype)

        return (stats_values, stats_counts)
