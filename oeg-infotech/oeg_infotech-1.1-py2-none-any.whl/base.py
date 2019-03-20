"""
Base classes for Infotech sections and items
"""
import csv
from StringIO import StringIO
from . import indent


def to_int(text):
    """
    text to int
    """
    try:
        return int(text)
    except ValueError:
        return ''


class AbstractItem(object):  # pylint: disable=too-few-public-methods
    """
    abstract class for xml item
    """
    def is_valid(self):
        """
        check for valid field values
        """
        return bool(self)


class DistItem(AbstractItem):
    """
    abstract class for item on dist
    """
    field_typeobj = 'IDTYPEOBJ'
    field_odometer = 'ODOMETER'
    field_comment = 'REM'
    # not required fields
    field_coord_longitude = 'L'
    field_coord_latitude = 'B'
    field_coord_height = 'H'
    field_coord_system = 'SRID'

    dist_attribs = [
      field_typeobj,
      field_odometer,
    ]

    coords_attribs = [
      field_coord_longitude,
      field_coord_latitude,
      field_coord_height,
      field_coord_system,
    ]

    def __init__(self):
        self.objtype = None
        self.dist = None
        self.comment = ''

        self.coord_longitude = None
        self.coord_latitude = None
        self.coord_height = None
        self.coord_system = None

    def fill_from_xml(self, xml_item):
        """
        fill item data from existing xml element
        """
        self.objtype = xml_item.attrib[DistItem.field_typeobj]
        self.dist = to_int(xml_item.attrib[DistItem.field_odometer])
        self.comment = xml_item.attrib[DistItem.field_comment]

        self.coord_longitude = xml_item.attrib.get(DistItem.field_coord_longitude, None)
        self.coord_latitude = xml_item.attrib.get(DistItem.field_coord_latitude, None)
        self.coord_height = xml_item.attrib.get(DistItem.field_coord_height, None)
        self.coord_system = xml_item.attrib.get(DistItem.field_coord_system, None)

    def as_csv_row(self, infotech, with_navigation=False):
        """
        return list of item fields for csv output
        """
        suffix = []
        if with_navigation:
            suffix = [
              self.coord_longitude,
              self.coord_latitude,
              self.coord_height,
              self.coord_system,
            ]

        return [
          infotech.obj_dict[self.objtype],
          "{}".format(self.dist),
          self.comment,
        ] + suffix

    def reverse(self, total_length, _object_index):
        """
        reverse object distance
        """
        self.dist = total_length - self.dist

    def base_xml(self, node):
        """
        set base attributes to xml node of object
        """
        node.set(DistItem.field_typeobj, self.objtype)
        node.set(DistItem.field_odometer, "{}".format(self.dist))
        node.set(DistItem.field_comment, self.comment)

        if self.coord_system is not None:
            node.set(DistItem.field_coord_longitude, self.coord_longitude)
            node.set(DistItem.field_coord_latitude, self.coord_latitude)
            node.set(DistItem.field_coord_height, self.coord_height)
            node.set(DistItem.field_coord_system, self.coord_system)


class Section(object):
    """
    abstract class for xml section
    """
    item_attributes = None

    def __init__(self, infotech, cls, section):
        self.infotech = infotech
        self.cls = cls
        self.section = section
        self._items = None

    @property
    def items(self):
        """
        lazy restore list of section's items
        """
        if self._items is None:
            self._items = []
            for obj in self.infotech.xml.getroot().find(self.section):
                item = self.cls.from_xml(obj)
                if item.is_valid():
                    self._items.append(item)

        return self._items

    def as_csv_body(self, title, column_titles, with_navigation=False):
        """
        dump section as csv string
        """
        output = StringIO()
        writer = csv.writer(output, delimiter=';', lineterminator='\n')

        writer.writerow([title] + ['' for _tmp in column_titles][1:])
        writer.writerow(column_titles)
        for item in self.items:
            writer.writerow([
              field.encode(self.infotech.codepage)
              for field in item.as_csv_row(self.infotech, with_navigation=with_navigation)
            ])

        content = output.getvalue()
        output.close()

        return content

    def rebuild_xml(self):
        """
        generate new xml data based on current section data
        """
        section = self.infotech.xml.getroot().find(self.section)
        section.clear()

        for item in self.items:
            node = item.add_xml_child(section)
            if self.item_attributes:
                node.ordered_attributes = self.item_attributes

    def reverse(self, total_length):
        """
        reverse vector of objects and modify self.infotech.xml
        """
        self._items = reversed(self.items)
        section = self.infotech.xml.getroot().find(self.section)
        section.clear()
        object_index = 1

        for item in self.items:
            item.reverse(total_length, object_index)
            item.add_xml_child(section)
            object_index += 1

        indent(section, level=1)

    def add_from_xml(self, xml_section, at_dist, dist_shift):
        """
        add objects from another infotech section from given dist
        """
        items = self.items
        for item in xml_section.items:
            item.dist = item.dist - dist_shift + at_dist
            items.append(item)
