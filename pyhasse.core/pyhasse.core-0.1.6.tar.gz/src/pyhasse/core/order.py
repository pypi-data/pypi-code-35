

import copy


class Order(object):
    """Order

    :param: | **datamatrix**
            | **rows**
            | **cols**

    Note, all numbers are referring to the rows of zeta-matrix
    which, in turn, is based on the representative elements
    but does not point to the complete set objects.
    Therefore call a certain row or column of zeta-matrix needs
    a loop
    ::

      for i in range(0, len(..))
          reducedlist[...[i]]

    """

    def __init__(self, datamatrix, rows, cols):
        self.datamatrix = datamatrix
        self.rows = rows
        self.cols = cols

    def sort_list(self, vector):
        """sorts a tuple of numbers 'vector'

        and trace back the permutations
        the vector will   n o  t  be overwritten

        :param list vector: list to be sorted (increasing values)
        :var sortedlist:

        source:raisort
        :var rows: number of objects (rows)
        :var vector: vector to be sorted
        :var sortvector: vector of components-nr
                ...of vector rearranged according to
                ...increasing values of components of
                ...vector.

        vector=[2,3,1,4,5] --> sortvector=[2,0,1,3,4]
        meaning that component 2 takes the lowest rank, component
        1 the next rank etc.
        :return sortedlist, sortvector: sorted vector,
                                        tracing back info (by sortvector)
        """

        rx = len(vector)
        sortvector = []
        sortedvector = []
        for i in range(0, rx):
            sortvector.append(0)
            sortedvector.append(0)

        sortedlist = copy.deepcopy(vector)
        sortedvector = copy.deepcopy(vector)
        for i in range(0, rx-1):
            for i1 in range(0, rx-1):
                if sortedlist[i1] >= sortedlist[i1 + 1]:  # 16.1.2015
                    h = sortedlist[i1 + 1]
                    sortedlist[i1 + 1] = sortedlist[i1]
                    sortedlist[i1] = h
        for i in range(0, rx):
            sortvector[i] = sortedvector.index(sortedlist[i])
            sortedvector[sortvector[i]] = str(sortedvector[sortvector[i]])
        return sortedlist, sortvector

    def calc_comparab(self, zeta):
        """ computes the comparabilities.

        Without equivalence relations, comparabilities and
        incomparabilities sum up to rows*(rows-1)/2.

        :var zeta: zeta matrix (square matrix)
        :var rows: number of rows / columns
        :return comparabilities: The number of all pais xi1 < xi2 with i1<i2
        """
        comparabilities = 0
        for i1 in range(0, self.rows):
            for i2 in range(0, self.rows):
                if zeta[i1][i2] == 1 and i1 != i2:
                    comparabilities += 1
        return comparabilities

    def calc_downset(self, zeta, rows):
        """ calculates the downset of an object, given a poset.

        :var zeta: square matrix of order relations of the
                   representative elements
        :var rows: rows (= columns) of matrix zeta
        :var downset: a two dimensional field of different lengths
                      containing a list of indices,pointing to
                      objects being members of the downsets
        :return downsets: set of object-indices
        """
        downsets = []
        for i1 in range(0, rows):
            downsets.append(0)
            downsets[i1] = []
            for i2 in range(0, rows):
                if zeta[i1][i2] != 0:
                    downsets[i1].append(i2)
        return downsets

    def calc_upset(self, zeta, rows):
        """ calculates the upset of an object, given a poset.

        :var zeta: square matrix of order relations of the
                   representative elements
        :var rows: rows (= columns) of matrix zeta
        :var upsets: a two dimensional field of different lengths
                      containing a list of indices,pointing to
                      objects being members of the downsets
        :return upsets: set of object-indices
        """
        upsets = []
        for i1 in range(0, rows):
            upsets.append(0)
            upsets[i1] = []
            for i2 in range(0, rows):
                if zeta[i2][i1] != 0:
                    upsets[i1].append(i2)
        return upsets

    def calc_incompset(self, zeta, rows):
        """calculates the set of incomparable elements each object
                ,out of the set of representative elements, has.

        :var incompset: 2D-field, for each row of zeta ...
                        its incomparable elements
        :return incompset: set of indices
        """
        incompsets = []
        for i1 in range(0, rows):
            incompsets.append(0)
            incompsets[i1] = []
            for i2 in range(0, rows):
                if zeta[i1][i2] == 0 and zeta[i2][i1] == 0:
                    incompsets[i1].append(i2)
        return incompsets

    def calc_relatmatrix(self, datamatrix, rows, cols, prec=9):
        """ calculates the relatmatrix from the data matrix 'datamatrix'

        :var rows:number of rows (objects)of x
        :var cols: number of columns (attributes) of x
                   or a list of some attributes
        :var relatmatrix: relatmatrix matrix (row >= column)
                          the relatmatrix is the zeta matrix when datamatrix
                          refers to the representants only
        :var flag: control of obj (i1) > obj(i2) for all attributes
        :return relatmstrix: relatmatrix or zeta matrix
        """

        if type(cols) == int:
            columns = [j for j in range(0, cols)]
        else:
            columns = cols

        relatmatrix = []
        for i in range(0, rows):
            relatmatrix.append(0)
            relatmatrix[i] = []
        flag = 0
        for i in range(0, rows):
            for i1 in range(0, rows):
                flag = 0

                for kk in columns:
                    if float(round(datamatrix[i][kk], prec)) >= \
                       float(round(datamatrix[i1][kk], prec)):
                        flag += 1
                if flag == len(columns):
                    relatmatrix[i].append(1)
                else:
                    relatmatrix[i].append(0)
        return relatmatrix

    def calc_cov(self, zeta, rows):
        """ generates the cover matrix from the zeta matrix

        :var zeta: zeta-matrix for the obj(i) >= obj(j)-relation
        :var rows: number of rows/columns of the square matrix zeta
        :var covd: matrix of the cover relation of >=, main diagonal: 1
        :var cov: matrix of the cover relation of >, main diagonal: 0
        :return: covd, cov
        """
        covd = []
        for i in range(0, rows):
            covd.append(0)
            covd[i] = []
        for i in range(0, rows):
            for i1 in range(0, rows):
                covd[i].append(zeta[i][i1])

        for i in range(0, rows):
            for i1 in range(0, rows):
                if i != i1:
                    for i2 in range(0, rows):
                        if i1 != i2:
                            # transitivity check
                            testsum = zeta[i][i1] + zeta[i1][i2]
                            if testsum > zeta[i][i2]:
                                covd[i][i2] = 0
        cov = []
        for i in range(0, rows):
            cov.append(0)
            cov[i] = []
        for i in range(0, rows):
            for i1 in range(0, rows):
                if i == i1:
                    cov[i].append(0)
                else:
                    cov[i].append(covd[i][i1])
        return covd, cov

    def calc_incomp(self, zeta, rows):
        """ Calculates the total incomparabilities, based on the zeta-matrix

        :var incomparable: number of incomparabilites
        :return: incomparable
        :type: int
        """
        incomp = 0
        for i in range(0, rows):
            for i1 in range(0, rows):
                if zeta[i][i1] == 0 and zeta[i1][i] == 0:
                    incomp += 0.5
        incomparable = int(incomp)
        return incomparable

    def calc_extremales(self, zeta, rows):
        """ Based on zeta-matrix calc. of extremales,

        i.e. maximal, minimal and isolated elements will be determined.
        based on the set of representative elements
        :var zeta: zeta-matrix (square matrix)
        :var rows: number of rows/columns of zeta-matrix
        :var minel:list of indices pointing to minimal elements
        :var maxel: list of indices pointing to maximal elements
        :var isoel: list of indices pointing to isolated elements
        :return: maxel, minel, isoel

        """
        maxel = []
        sumel = []
        for i1 in range(0, rows):
            sumtest = 0
            for i in range(0, rows):
                sumtest += zeta[i][i1]
            sumel.append(sumtest)
            if sumel[i1] == 1:
                maxel.append(i1)
        minel = []
        sumel = []
        for i in range(0, rows):
            sumtest = 0
            for i1 in range(0, rows):
                sumtest += zeta[i][i1]
            sumel.append(sumtest)
            if sumel[i] == 1:
                minel.append(i)
        isoel = []
        for iob in minel:
            if iob in maxel:
                isoel.append(iob)
        return maxel, minel, isoel

    def calc_level(self, zeta, rows):
        """ Calculates the colevels of a partial order

        after Patil, Taillie, 2004.

        :var zeta: zeta-matrix (square matrix)
        :var zetatr: transposed zetamatrix (square matrix)
        :var rows:number of rows/columns
        :var summe:columnsum of zetatr
        :var listhilf: interim result to store
                       objects having the same value in summe
        :var tps:already visited vertices
        :var levobj: levobj is a field, components;
                     indices pointing to objects in
                     the different levels, main result
                     ** Note:** vpmponents (which are themselves lists)
                     are ordered from top to bottom
        """

        zetatr = []
        for i1 in range(0, rows):
            zetatr.append(0)
            zetatr[i1] = []
        for i1 in range(0, rows):
            for i2 in range(0, rows):
                zetatr[i1].append(zeta[i2][i1])

        levobj = []
        tps = []
        lx = 1
        while lx > 0:
            listhilf = []
            for i1 in range(0, rows):
                    summe = 0
                    if i1 not in tps:
                        for i2 in range(0, rows):
                            if i2 not in tps:
                                summe += zetatr[i1][i2]
                        if summe == 1:
                            listhilf.append(i1)
            if listhilf != []:
                levobj.append(listhilf)
            lx = len(listhilf)
            tps.extend(listhilf)
        return levobj

    def calc_maxlevel(self, levobj):
        """ the largest level is searched and the number
        of its objects is calculated
        :var levobj: a field where the obects are assigend to levels
        :var maxlev: how many objects in the largest level
        """
        maxlev = -10**20
        for i in range(0, len(levobj)):
            if len(levobj[i]) > maxlev:
                maxlev = len(levobj[i])
        return maxlev
