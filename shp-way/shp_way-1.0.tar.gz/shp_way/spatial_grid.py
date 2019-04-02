import math
from statistics import median


class SpatialGrid:
    """"
    Class represents a spatial grid based on inputted attributes

    Public Attributes
    ------------------
    - grid: data structure representing the spatial grid
    - absolute_max: upper left coordinate of the grid
    - absolute_min: lower right coordinate of the grid
    - num_rows: number of rows presented in the grid
    - num_cols: number of columns presented in the grid

    'Private' Attributes
    ------------------
    - absolute_width: the medium value from a list of widths used for auto-generating number of columns in grid
    - absolute_height: the medium value from a list of heights used for auto-generating number of rows in grid
    - x_max: the max x coordinate
    - y_max: the max y coordinate
    - x_min: the min x coordinate
    - y_min: the min y coordinate

    """
    def __init__(self, abs_max, abs_min, heights, widths, num_rows=None, num_cols=None):
        """
        Parameters
        ----------
        :param abs_max : float
            absolute max coordinate for grid
        :param abs_min: float
            absolute min coordinate for grid
        :param heights: list (int)
            list of height values to approximate median cell size
        :param widths: list (int)
            list of width values to approximate median cell size
        :param num_rows: int, optional
            number of rows to be used for grid instead of auto-generating the value
        :param num_cols: int, optional
            number of rows to be used for grid instead of auto-generating the value
        """
        self.__absolute_max = None
        self.__absolute_min = None

        self.__absolute_height = None
        self.__absolute_width = None

        self.__grid = list()

        self.__grid_padding(abs_max, abs_min)

        self.__x_max = self.__absolute_max[0]
        self.__y_max = self.__absolute_max[1]

        self.__x_min = self.__absolute_min[0]
        self.__y_min = self.__absolute_min[1]

        if (isinstance(num_rows, int) and num_rows > 1) and (isinstance(num_cols, int) and num_cols > 1):
            self.__num_rows = num_rows
            self.__num_cols = num_cols
        else:
            self.__calculate_num_rows_cols(median(widths), median(heights))
        self.__create_spatial_grid(self.__num_rows, self.__num_cols)

    @property
    def grid(self):
        return self.__grid

    @property
    def absolute_max(self):
        return self.__absolute_max

    @property
    def absolute_min(self):
        return self.__absolute_min

    @property
    def num_rows(self):
        return self.__num_rows

    @property
    def num_cols(self):
        return self.__num_cols

    def __grid_padding(self, abs_max, abs_min):
        """
        Slightly pad grid boundaries to ensure all objects are covered by the spatial grid
        :param abs_max: tuple of floats
            the upper left vertex of the grid
        :param abs_min: tuple of floats
            the lower right vertex of the grid
        :return: None
        """
        abs_min = min(abs_max, abs_min)
        abs_max = max(abs_max, abs_min)

        x_max_temp = abs_max[0] + .00000001
        y_max_temp = abs_max[1] + .00000001
        x_min_temp = abs_min[0] + .00000001
        y_min_temp = abs_min[1] + .00000001

        self.__absolute_max = (x_max_temp, y_max_temp)
        self.__absolute_min = (x_min_temp, y_min_temp)

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

    def __calculate_abs_len_width(self):
        """
        Calculate the median size of the width and height from the widths and heights parameters
        :return: None
        """
        self.__absolute_width = self.distance_calculation(self.__absolute_min, (self.__x_max, self.__y_min))
        self.__absolute_height = self.distance_calculation((self.__x_max, self.__y_min), self.__absolute_max)

    def __calculate_num_rows_cols(self, median_width, median_height):
        """
        Determine the number of rows and cols by finding the fixed size of each cell in the grid
        :param median_width: list of floats
        :param median_height: list of floats
        :return: None
        """
        self.__calculate_abs_len_width()

        self.__num_rows = int(self.__absolute_height / median_height)
        self.__num_cols = int(self.__absolute_width / median_width)

    def __create_spatial_grid(self, num_rows, num_cols):
        """
        Create a grid based on a given value for the number of rows and columns
        :param num_rows: int
            number of rows
        :param num_cols: int
            number of columns
        :return: None
        """
        self.__grid = list()

        for row in range(num_rows):
            temp_row = list()
            for col in range(num_cols):
                temp_col = list()
                temp_row.append(temp_col)
            self.__grid.append(temp_row)
