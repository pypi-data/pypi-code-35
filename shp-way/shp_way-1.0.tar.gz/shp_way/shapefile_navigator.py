from shp_way import collision_detection, path_finder, read_shp
import matplotlib.pyplot as plt
import mplleaflet
import random


class ShapefileNavigator:
    """
    Class represents a tool that converts shapefiles to a working navigation system. Size of spatial grid used for the
    system can be set to a fixed size or auto-generated.

    'Private' Attributes
    ------------------
    - r_obj: ReadShapeFiles object
    - collision_obj: CollisionDetection object


    Example of class usage:
    ShapefileNavigator('C:/Username/documents/shapefile_folder/roads',
                       'C:/Username/documents/shapefile_folder/buildings')
        - size of grid will be auto-generated due to not providing a value

    ShapefileNavigator('C:/Username/documents/shapefile_folder/roads',
                       'C:/Username/documents/shapefile_folder/buildings', rows=15, cols=20)

        - setting values for the rows and cols will create a fixed size set of cell partitions in the grid
        - 15 rows and 20 cols creates 300 cell partitions used for the spatial grid. Size of spatial grid can affect
        efficiency and processing speeds
    """
    def __init__(self, pathway_shapefile, visitation_shapefile, rows=None, cols=None):
        """
        Parameters
        ----------
        :param pathway_shapefile: string
            shapefile describing the pathways
        :param visitation_shapefile: string
            shapefile describes all potential visitation objects or destinations
        :param rows: int, optional
             number of rows to be used for grid instead of auto-generating the value
        :param cols: int, optional
             number of columns to be used for grid instead of auto-generating the value
        """

        self.__r_obj = read_shp.ReadShapeFiles(pathways=pathway_shapefile, destinations=visitation_shapefile)
        self.__collision_obj = collision_detection.CollisionDetection(self.__r_obj, rows=rows, cols=cols)

    def get_rows_cols(self):
        """
        Get the rows and columns used for the spatial grid for the shapefile navigation system
        :return: tuple of the number of rows and columns
        """

        return self.__collision_obj.num_rows(), self.__collision_obj.num_cols()

    def get_graph(self):
        """
        Get the shapefile graph used for the navigation system
        :return: NetworkX graph
        """

        return self.__collision_obj.shp_graph.graph

    def get_reference_directory(self):
        """
        Get the reference directory for all visitation objects
        :return: hash table containing all information regarding each visitation object
        """

        return self.__collision_obj.shp_graph.reference_directory

    def show_directory(self):
        """
        Print all potential areas of visitation
        :return: None
        """

        directory = self.get_reference_directory()
        for i in directory.keys():
            print(i)

    @staticmethod
    def get_algorithms():
        """
        Get all available algorithms
        :return: enum class containing all available algorithms
        """

        return path_finder.ShortestPathAlgorithm

    def find_path(self, src, dst, algorithm=path_finder.ShortestPathAlgorithm.dijkstra):
        """
        Calculate the path between src and dst using a supported path finding algorithm
        :param src: string
            the source or starting point for navigation
        :param dst: string
            the destination or ending point for navigation
        :param algorithm: ShortestPathAlgorithm attribute, optional (defaulted to Dijkstra's)
            algorithm used for path finding
        :return: list of NetworkX nodes outlining shortest path between src and dst
        """

        directory = self.get_reference_directory()
        if directory.get(src) is None or directory.get(dst) is None:
            raise read_shp.ShapeFileNavigatorException("src or dst is not present in reference directory")
        path = path_finder.nx_shortest_path(self.get_graph(), directory[src]['entry_nodes'],
                                            directory[dst]['entry_nodes'], alg_name=algorithm)
        return path

    def show_path(self, src, dst, algorithm=path_finder.ShortestPathAlgorithm.dijkstra,
                  show_graph=False, show_entry_points=True):
        """
        Calculate and display the path between src and dst using a supported path finding algorithm.
        :param src: string
            the source or starting point for navigation
        :param dst: string
            the destination or ending point for navigation
        :param algorithm: ShortestPathAlgorithm attribute, optional (defaulted to Dijkstra's)
            algorithm used for path finding
        :param show_graph: boolean, optional
            outline the NetworkX graph in which path finding takes place on
        :param show_entry_points: boolean, optional
            outline all potential entry points between src and dst
        :return: None
        """

        path = self.find_path(src, dst, algorithm=algorithm)
        if path is None:
            raise read_shp.ShapeFileNavigatorException("path does not exist")

        if show_graph:
            color = 'blue'
            line_width = 5
        else:
            color = (random.uniform(0, .5), random.uniform(0, .5), random.uniform(0, .5))
            line_width = 2

        x = list()
        y = list()
        for i in path:
            x.append(i[0])
            y.append(i[1])

        plt.plot(x, y, color=color, linestyle='solid', marker='o', linewidth=line_width)

        if show_graph is True:
            graph = self.get_graph()
            pos = path_finder.nx.get_node_attributes(graph, 'pos')
            path_finder.nx.draw(graph, pos, node_size=10)
            path_finder.nx.draw_networkx_labels(graph, pos, font_size=5, font_family='sans-serif')

        if show_entry_points is True:
            x_coordinates = [path[0][0], path[-1][0]]
            y_coordinates = [path[0][1], path[-1][1]]
            plt.scatter(x=x_coordinates, y=y_coordinates, color=color, marker='D')

        mplleaflet.show()
