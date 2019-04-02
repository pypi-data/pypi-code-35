import shapefile
import networkx as nx
from shapely.geometry import Polygon, box
import math


"""Shapefile Represented Types"""
NULL = 0
POINT = 1
POLYLINE = 3
POLYGON = 5
MULTIPOINT = 8
POINTZ = 11
POLYLINEZ = 13
POLYGONZ = 15
MULTIPOINTZ = 18
POINTM = 21
POLYLINEM = 23
POLYGONM = 25
MULTIPOINTM = 28
MULTIPATCH = 31


class ShapeFileNavigatorException(Exception):
    pass


class ReadShapeFiles:
    """
    Class represents an object to contain two PyShp objects while ensuring shapefiles are supported

     Public Attributes
    ------------------
    - pathways_sf: PyShp object containing pathways shapefile
    - destinations_sf: PyShp object containing the destinations shapefile
    """
    def __init__(self, pathways="shapefiles/roads", destinations="shapefiles/buildings"):
        """
        Parameters
        ----------
        :param pathways: string, optional if shapefiles are present in 'shapefiles/' code directory
            directory containing shapefile
            example: 'C:/Username/documents/shapefile_folder/roads'

        :param destinations: destinations: string, optional if shapefiles are present in 'shapefiles/' code directory
            directory containing shapefile
            example: 'C:/Username/documents/shapefile_folder/buildings'
        """
        self.__pathways_sf = None
        self.__destinations_sf = None
        self.__integrity_check(pathways, destinations)

    @property
    def pathways_sf(self):
        """
        :return: shapefile containing pathways
        """
        return self.__pathways_sf

    @property
    def destinations_sf(self):
        """
        :return: shapefile containing visitation objects
        """
        return self.__destinations_sf

    def __integrity_check(self, pathways, destinations):
        """
        Ensure given shapefiles are supported and are aligned
        :param pathways: string
            Shapefile containing polyline shapes
        :param destinations: string
            Shapefile containing polygon shapes (Currently)
        :return: None
        """
        pathways_sf = self.__read_files(pathways)
        destinations_sf = self.__read_files(destinations)

        p_bbox = box(pathways_sf.bbox[0], pathways_sf.bbox[1], pathways_sf.bbox[2], pathways_sf.bbox[3])
        v_bbox = box(destinations_sf.bbox[0], destinations_sf.bbox[1], destinations_sf.bbox[2], destinations_sf.bbox[3])

        if pathways_sf.shapeType == POLYLINE and destinations_sf.shapeType == POLYGON:
            if p_bbox.intersects(v_bbox):
                self.__pathways_sf = pathways_sf
                self.__destinations_sf = destinations_sf
            else:
                raise ShapeFileNavigatorException("Scope of included shapefiles are not aligned")
        elif pathways_sf.shapeType == POLYGON and destinations_sf.shapeType == POLYLINE:
            if v_bbox.intersects(p_bbox):
                self.__pathways_sf = destinations_sf
                self.__destinations_sf = pathways_sf
            else:
                raise ShapeFileNavigatorException("Scope of included shapefiles are not aligned")
        else:
            raise ShapeFileNavigatorException("The included shapefiles are not supported")

    @staticmethod
    def __read_files(file_path):
        """
        Apply shapefile reader to main file
        :param file_path: string
            main file selected
        :return: PyShp reader of given file_path
        """
        sf = shapefile.Reader(file_path)
        return sf


class ShapefileGraph:
    """
    Class represents a graph and reference directory generated from shapefiles using a ReadShapefile object

    Public Attributes
    ------------------
    - bb_max: maximum bounding boxes vertex value from all visitation objects' polygon's
    - bb_min: minimum bounding boxes vertex value from all visitation objects' polygon's
    - polygon_widths: all visitation objects' polygon's bounding box's width
    - polygon_heights: all visitation objects' polygon's bounding box's height
    - graph: NetworkX graph object
    - reference directory: hash table data structure used to reference all visitation objects' polygon, cell partitions,
    and entry points
    """
    def __init__(self, readshp_obj):
        """
        Parameters
        ----------
        :param readshp_obj: ReadShapefiles object
            a ReadShapefiles object containing the shapefiles
        """
        self.__bb_max = None
        self.__bb_min = None

        self.__polygon_widths = list()
        self.__polygon_heights = list()

        self.__graph = nx.Graph()
        self.__reference_directory = dict()
        self.__process(readshp_obj)

    @property
    def bb_max(self):
        return self.__bb_max

    @property
    def bb_min(self):
        return self.__bb_min

    @property
    def polygon_widths(self):
        return self.__polygon_widths

    @property
    def polygon_heights(self):
        return self.__polygon_heights

    @property
    def graph(self):
        return self.__graph

    @property
    def reference_directory(self):
        return self.__reference_directory

    def __process(self, read_shp_obj):
        """
        Initialize the process to create the shapefile graph and reference directory
        :param read_shp_obj: ReadShapefile object
        :return: None
        """
        if not isinstance(read_shp_obj, ReadShapeFiles):
            raise ShapeFileNavigatorException("Given object is not supported. Please use a ReadShapefiles object")

        self.__process_polygons(read_shp_obj.destinations_sf)
        self.__process_poly_lines(read_shp_obj.pathways_sf)

        min_x = min(read_shp_obj.pathways_sf.bbox[0], read_shp_obj.destinations_sf.bbox[0])
        min_y = min(read_shp_obj.pathways_sf.bbox[1], read_shp_obj.destinations_sf.bbox[1])

        max_x = max(read_shp_obj.pathways_sf.bbox[2], read_shp_obj.destinations_sf.bbox[2])
        max_y = max(read_shp_obj.pathways_sf.bbox[3], read_shp_obj.destinations_sf.bbox[3])

        self.__bb_max = (max_x, max_y)
        self.__bb_min = (min_x, min_y)

    def __process_polygons(self, sf):
        """
        Process shapefiles containing polygons
        :param sf: PyShp object
            PyShp object containing the polygon shapefile
        :return: None
        """
        records = list(sf.iterRecords())
        counter = 0

        for i, shape in enumerate(sf.iterShapeRecords()):
            self.__calculate_polygon_size(shape.shape.bbox)
            name = records[i][1]

            if name.strip() is '':
                counter += 1
                name = "Unknown {}".format(counter)

            self.__reference_directory[name.strip()] = {
                'assigned_cell_partitions': list(),
                'shp_reference':  Polygon(shape.shape.points),
                'entry_nodes': list()
            }

    def __calculate_polygon_size(self, bbox):
        """
        Calculate the width and height of a polygon's bounding box
        :param bbox: list of floats
            bounding box of a polygon
        :return: None
        """
        mn_x = bbox[0]
        mn_y = bbox[1]
        mx_x = bbox[2]
        mx_y = bbox[3]

        mn = (mn_x, mn_y)
        mn_x_mx_y = (mx_x, mn_y)
        mx = (mx_x, mx_y)

        width = self.distance_calculation(mn, mn_x_mx_y)
        height = self.distance_calculation(mn_x_mx_y, mx)

        self.__polygon_widths.append(width)
        self.__polygon_heights.append(height)

    def __process_poly_lines(self, sf):
        """
        Process shapefiles containing polylines
        :param sf: PyShp object
            PyShp object containing the polyline shapefile
        :return: None
        """
        for shape in sf.iterShapeRecords():
            prev_point = None
            counter = 0

            for point in shape.shape.points:
                self.__graph.add_node(point, pos=point)
                if counter > 0:
                    self.__graph.add_edge(prev_point, point, weight=self.distance_calculation(prev_point, point))
                prev_point = point
                counter += 1

    @staticmethod
    def midpoint(x1, y1, x2, y2):
        """
        Calculate the midpoint using x and y values
        :param x1: float
            first x value
        :param y1: float
            first y value
        :param x2: float
            second x value
        :param y2: float
            second y value
        :return: midpoint
        """
        coord = ((x1 + x2)/2, (y1 + y2)/2)
        return coord

    @staticmethod
    def distance_calculation(coord1, coord2):
        """
        Calculate the distance between two coordinates
        :param coord1: tuple of floats
            first coordinate
        :param coord2: tuple of floats
            second coordinate
        :return: distance
        """
        x1 = coord1[0]
        y1 = coord1[1]
        x2 = coord2[0]
        y2 = coord2[1]
        return math.hypot(x2 - x1, y2 - y1)
