"""
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3


class Triangle():
    """
    A Triangle is defined by three apexes
    - apex 0
    - apex 1
    - apex 2

    This class provides methods to calculate triangle properties when the \
    apexes of a triangle are known
    """

    def __init__(self, apex0, apex1, apex2):
        msg = 'should be a pandas Series with x,y,z as index'
        if not isinstance(apex0, pd.Series):
            raise TypeError('apex0 ' + msg)
        if not isinstance(apex1, pd.Series):
            raise TypeError('apex1 ' + msg)
        if not isinstance(apex2, pd.Series):
            raise TypeError('apex2 ' + msg)
        if apex0.shape[0] != 3:
            raise IOError('apex0 ' + msg)
        if apex1.shape[0] != 3:
            raise IOError('apex1 ' + msg)
        if apex2.shape[0] != 3:
            raise IOError('apex2 ' + msg)
        if ('x' not in apex0.index) or \
           ('y' not in apex0.index) or \
           ('z' not in apex0.index):
            raise IOError('apex0 ' + msg)
        if ('x' not in apex1.index) or \
           ('y' not in apex1.index) or \
           ('z' not in apex1.index):
            raise IOError('apex1 ' + msg)
        if ('x' not in apex2.index) or \
           ('y' not in apex2.index) or \
           ('z' not in apex2.index):
            raise IOError('apex2 ' + msg)
        if apex0.dtype != float:
            raise IOError('apex0 does not contains float')
        if apex1.dtype != float:
            raise IOError('apex1 does not contains float')
        if apex2.dtype != float:
            raise IOError('apex2 does not contains float')

        # The apexes are stored in a pandas dataframe
        self.apexes = pd.DataFrame(index=['x', 'y', 'z'],
                                   columns=['apex0', 'apex1', 'apex2'],
                                   dtype=float)
        self.apexes.apex0 = apex0
        self.apexes.apex1 = apex1
        self.apexes.apex2 = apex2

    def __convert_list2array(self, clist):
        if isinstance(clist, list):
            clist = np.array(clist)
        return clist

    def center_of_mass(self):
        """center of mass

        :returns: center of mass of the triangle
        :rtype: pandas series

        """
        cm = pd.Series(index=['x', 'y', 'z'], name='center_of_mass')
        cm.x = self.apexes.loc['x', :].mean()
        cm.y = self.apexes.loc['y', :].mean()
        cm.z = self.apexes.loc['z', :].mean()
        return cm

    def apexes2vectors(self):
        """apexes2vectors return a vector between each apexes
        the vector originating from apex a and going to apex b, \
can be access as (a,b), here a and b are the apex index.
        for example for the vector between apex0 and apex1, \
the tuple is (0,1)

        :returns: return the vectors between edges
        :rtype: pandas multiindexed DataFrame

        """
        vec = pd.DataFrame(data=0,
                           index=['x', 'y', 'z'],
                           columns=pd.MultiIndex.from_tuples([(0, 1),
                                                              (1, 2),
                                                              (2, 0)]))
        vec.name = 'vectors'
        vec.loc[:, (0, 1)] = self.apexes.apex1 - self.apexes.apex0
        vec.loc[:, (1, 2)] = self.apexes.apex2 - self.apexes.apex1
        vec.loc[:, (2, 0)] = self.apexes.apex0 - self.apexes.apex2
        return vec

    def apexes2edges_norm(self):
        """apexes2edges_norm return the edges norm.

        the edges are accessed by a tuple (a,b), here a and b \
are the apex indeces.
        for example for the edge between apex0 and apex1, the \
tuple is (0,1)

        :returns: return edges norm
        :rtype: pandas multindexed Series

        """
        en = self.apexes2vectors()
        en = np.sqrt((en**2).sum(axis=0))
        en.name = 'edges_norm'
        return en

    def medians(self):
        """medians
        :returns: the point on the facing edge of an apex at which the median \
        emanating from this apex cross the facing edge.
        :rtype: pd.dataframe
        """
        md = pd.DataFrame(index=['x', 'y', 'z'],
                          columns=[0, 1, 2])
        vec = self.apexes2vectors()
        md.loc[:, 0] = (vec.loc[:, (1, 2)] / 2) + self.apexes.apex1
        md.loc[:, 1] = (vec.loc[:, (2, 0)] / 2) + self.apexes.apex2
        md.loc[:, 2] = (vec.loc[:, (0, 1)] / 2) + self.apexes.apex0
        return md

    def transform(self, matrix):
        if not isinstance(matrix, (np.ndarray, np.generic)):
            raise TypeError('frame should be a numpy array')
        if len(matrix.shape) != 2:
            raise TypeError('frame should have 2 dimensions')
        if not np.all(matrix.shape == [4, 4]):
            matrix = matrix[:3, :]
        if not np.all(matrix.shape != [3, 4]):
            raise TypeError('frame should be a 3x4 or 4x4 matrix')
        for apexname, row in self.apexes.transpose().iterrows():
            self.apexes.loc[['x', 'y', 'z'], apexname] = matrix.dot(
                [row.x, row.y, row.z, 1])[:3]

    def plot(self, ax=plt.gca(),
             facecolor='k',
             edgecolor='k',
             alpha=1,
             apex_marker=None):
        vtx = np.zeros((3, 3))
        vtx[:, 0] = self.apexes.apex0.values
        vtx[:, 1] = self.apexes.apex1.values
        vtx[:, 2] = self.apexes.apex2.values
        tri = a3.art3d.Poly3DCollection([vtx.transpose()])
        tri.set_facecolor(facecolor)
        tri.set_edgecolor(edgecolor)
        tri.set_alpha(alpha)
        ax.add_collection3d(tri)
        if apex_marker is not None:
            for _, row in self.apexes.transpose().iterrows():
                plt.plot([row.x], [row.y], [row.z], apex_marker)
        xlim = list(ax.get_xlim())
        ylim = list(ax.get_ylim())
        zlim = list(ax.get_zlim())
        if min(xlim) < min(vtx[0, :]):
            xlim[0] = min(vtx[0, :])
        if max(xlim) > max(vtx[0, :]):
            xlim[1] = max(vtx[0, :])
        if min(ylim) < min(vtx[1, :]):
            ylim[0] = min(vtx[1, :])
        if max(ylim) > max(vtx[1, :]):
            ylim[1] = max(vtx[1, :])
        if min(zlim) < min(vtx[2, :]):
            zlim[0] = min(vtx[2, :])
        if max(xlim) > max(vtx[2, :]):
            zlim[1] = max(vtx[2, :])
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)
