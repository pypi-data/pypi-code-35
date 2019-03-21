
class CSVReader(object):
    """ Read Data from csv files and convert the data to a matrix

    :param  fn: Filename (incl. path)
    :var obj: list of object names
    :var a: field of the csv-File (inclus. att and obj names)
    :var la: all rows (inclus. names of attributes)
    :var ls: all columns (inclus. names of objects)
    :var dm: interim field of entries of csv-file
    :var formval: values taken from a formular (string)
    :var ndec: number of decimals (precision)
    """

    def __init__(self, fn=None, formval=None, ndec=3, demo=None):

        self.DEMO = demo
        self.fn = fn
        self.repr_obj = {}
        self.repr_prop = {}
        self.formval = formval
        self.max = 0
        self.ndec = ndec
        self.eqm = []
        self.prop = []
        self.obj = []
        self.cols = 0
        self.rows = 0
        self.data = []
        self.skiped_rows = []
        self.redrows = 0
        self.missing_data = False
        self.missing_attr = False
        self.delimiter = None
        self.dmdim()

    def calc_reduced_system(self, prec=3):
        """ calculate values used uses from other funtions

        based on a reduced list with equivalence objects"""

        #  names convention
        # ================================================================
        # new name     old name       example                 former names
        # self.reddm   data, dm
        # self.redrows rowsred, rred  <number of representants>       rred
        # self.redobj  rlist           0,2.4,...   rlist
        # self.objred                  a,c,e,...
        # self.obj                     a,b,c,d,....
        # self.rows    r              <number of all objects>
        # zeta         relat

        self.eqm, self.redrows = self.generate_equivalenceclasses(self.data,
                                                                  self.rows,
                                                                  self.cols,
                                                                  prec)
        self.redobj = self.find_representative_elements(self.eqm)
        self.dmred = self.calc_dmred(self.data, self.redobj, self.cols)
        self.objred = [self.obj[i] for i in self.redobj]
        self.eqcl = self.generate_eqcl(self.obj, self.eqm)

        
    def read_string(self):
        """Load csv data from string

        :var max: filter lines, not as long as the header"""

        formval = self.formval.split('\n')
        if len(formval) < 2:
            self.missing_data = True
            return
        # firstline for delimiter
        for j in [',', '\t', ';', ' ']:
            firstline = formval[0].strip().split(j)
            firstlinevalues = [i for i in firstline if i != ""]
            secondline = formval[1].strip().split(j)
            secondlinevalues = [i for i in secondline if i != ""]

            # if the upper left corner is not filled
            if len(secondlinevalues) == len(firstlinevalues)+1:
                values = [""] + firstlinevalues
            else:
                values = firstlinevalues
            if len(values) > 1:
                counter = 1
                for i in values:
                    counter += 1
                self.max = len(values)
                self.delimiter = j
                break
        self.prop, renamed_attributes = self._rename_double(values[1:])
        obj_names = []
        for i in range(1, len(formval)):
            line = formval[i].strip().split(self.delimiter)
            values = [j for j in line if j.strip() != ""]
            if len(values) != self.max:
                self.skiped_rows.append([i,
                                         len(values),
                                         formval[i]])
            else:
                try:
                    floats = [float(k.replace(',', '.')) for k in values[1:]]
                    self.data.append(floats)
                    obj_names.append(values[0])
                except Exception:
                    pass

        self.obj, renamed_objects = self._rename_double(obj_names)
        self._demomode()
        self.rows = len(self.obj)
        self.cols = len(self.prop)
        # check minimum of data
        if self.rows > 1:
            self.missing_data = False
        else:
            self.missing_data = True
            msg = ['',
                   '',
                   '<p><em>Not enough rows</em>, check your data</p>']
            self.skiped_rows.append(msg)

        if self.cols > 0:
            self.missing_attr = False
        else:
            self.missing_attr = True
            msg = ['',
                   '',
                   '<p><em>Not enough attributes </em>, check your data']
            self.skiped_rows.append((msg))
        if renamed_objects or renamed_attributes:
            msg = ['',
                   '',
                   '<p>Some names are identical and renamed</p>']
            self.skiped_rows.append((msg))

    def _demomode(self):
        """Cut the number of rows and colums to a given value"""
        if self.DEMO:
            demodata = []
            if self.DEMO > len(self.data):
                maxrows = len(self.data)
            else:
                maxrows = self.DEMO
            for i in range(maxrows):
                demodata.append(self.data[i][:maxrows])
            if self.DEMO > len(self.prop):
                maxcols = len(self.prop)
            else:
                maxcols = self.DEMO

            self.data = demodata
            self.prop = self.prop[:maxcols]
            self.obj = self.obj[:maxrows]

    def dmdim(self):
        """Dimension of the read-in datamatrix"""

        if self.fn:
            fhd = open(self.fn, 'r')
            with fhd:
                self.formval = fhd.read()
            fhd.close()
        self.read_string()

    def generate_equivalenceclasses(self, dm, rows, cols, prec=None):
        """calculates the dm of the quotient set

        And gives a list of equivalence classes

        adapted for the new PyHasse-core

        :var dm: entries  of data matrix
        :var rows:  number of rows (i.e. of objects)
        :var rowsred: number of rows corresponding to the representants
        :var cols: number of columns (i.e. of attributes)
        :var eqm: an irregular 2-dim field, i.e. lists
                    of different length within a list
        :var already_visited: list of visited object
                               indices in the i2-loop
        :var help: list generated for any i1 not already visited
        :return: eqm, rowsred
        """
        eqm = []
        if prec:
            for i in range(0, rows):
                for j in range(0, cols):
                    dm[i][j] = round(dm[i][j], prec)

        # the proper block to calculate equivalence classes
        # idea: objects (their indices) already visited in the
        # second loop will no more visited by the first loop

        already_visited = []
        for i1 in range(0, rows):
            if i1 not in already_visited:
                help = []
                help.append(i1)
                for i2 in range(i1+1, rows):
                    if dm[i1] == dm[i2]:
                        help.append(i2)
                        already_visited.append(i2)
                eqm.append(help)
        rred = len(eqm)
        return eqm, rred

    def find_representative_elements(self, eqm):
        """ given eqm of the method 'generate_equivalence_classes'

        representative elements are selcted.

        :var eqm: list of lists. The sublists may have different lengths
        :var reqm: length of list eqm
        :return: reducedlist list of representants
        """
        reducedlist = []
        reqm = len(eqm)
        for i1 in range(0, reqm):
            reducedlist.append(eqm[i1][0])
        return reducedlist

    def calc_dmred(self, dm, reducedlist, cols):
        """ based on 'reducedlist' of method 'find_representative_elements'

        the data matrix is reduced. After calc_dmred the data matrix
        contains only the values of the representaitve elements

        :param list reducedlist: result of method 'find_repres._elements'
        :var dm: data matrix haveing eventually equivalent rows
        :var dmred: reduced data matrix, based on representative
                    elements of each equivalence class
        """
        dmred = []
        rowsred = len(reducedlist)
        for i in range(0, rowsred):
            dmred.append(0)
            dmred[i] = []
        iz1 = 0
        for i in reducedlist:
            for j in range(0, cols):
                dmred[iz1].append(dm[i][j])
            iz1 += 1

        return dmred

    def matrixredukt(self, rowcol):
        """ calcutlates a reduced square matrix

        by eliminating the rowcol th row and rowcol column from x

        :param rowcol: the row/column to be eliminated from x

        :var x: square matrix with r rows and columns
        :var r: number of rows (and columns)
        :return: reduct
        """
        self.xreduct = []
        for i1 in range(0, self.rows-1):
            self.xreduct.append(0)
            self.xreduct[i1] = []
        iz1 = 0
        for i1 in range(0, self.rows):
            iz2 = 0
            for i2 in range(0, self.rows):
                if (i1 != rowcol) and (i2 != rowcol):
                    self.xreduct[iz1].append(self.matrix[i1][i2])
                    iz2 += 1
            if i1 != rowcol:
                iz1 += 1
        return self.xreduct

    def assign_labels(self, result, reducedlist):
            """ Results (in 'result' based on zeta-matrix need a relabelling,

            according to the actual list of representative
            elements ('reducelist').

            :param list result: a list (no other sublists)
            :param list reducedlist: list of representative elements
            """
            self.assignedlist = []
            for i in range(0, len(result)):
                self.assignedlist.append(reducedlist[result[i]])
            return self.assignedlist

    def assign_labels_fields(self, resultfield, reducedlist):
        """ Results (in 'resultfield' based on zeta-matrix need a relabelling,

        according to the actual list of representative elements ('reducelist').

        :param resultfield: a list (there may be other sublists)
        :param reducedlist: list of representative elements
        :return: assignedfield: a field, corresponding to the structure
                                of 'result'
        """
        self.assignedfield = []
        for i in range(0, len(resultfield)):
            self.assignedfield.append(0)
            self.assignedfield[i] = []
        for i in range(0, len(resultfield)):
            for i1 in range(0, len(resultfield[i])):
                self.assignedfield[i].append(reducedlist[resultfield[i][i1]])
        return self.assignedfield

    def generate_objred(self, reducedlist):
        """ when a list of labels of representative elements is given,

        then a list of corresponding object-short-names is provided

        :var self.obj: is the complete list of object-short-names
        :var reducedlist: an actual list of labels
        :return objredlist: the reducedlist of labels
                            gets the object-short-names
        """
        objredlist = []
        for i in reducedlist:
            objredlist.append(self.obj[i])
        return objredlist

    def weak(self, obj, objred, eqm, flist):
        """ Extends a list, calculated for the reduced
        list to a klist related to all objects
        Assume the equivalence classes [a, d, e], [b, f], [c] and
        flist has the values for the representative elements a,b,c
        namely flist(a) = 2, flist(b) = 1, flist(c) =  3, then the
        extendedlist fextlist is: fextlist(a) = 2, fextlist(b) = 1,
        fextlist(c) = 3, fextlist(d) = 2, fextlist(e) = 2
        :var obj: original (full) list of objects
        :var objred: reduced list of represeantants
        :var eqm: list of equivalence classes
        :var flist: one-dimensional list of numbers related to objred
        :return fextlist
        :rtyp tuple
        """
        rows = len(obj)
        fextlist = []
        for i in range(0, rows):
            fextlist.append(0)

        for ob in objred:
            iob = obj.index(ob)
            fextlist[iob] = flist[objred.index(ob)]
        for i in range(0, len(eqm)):
            for i1 in eqm[i]:
                fextlist[i1] = fextlist[eqm[i][0]]
        return fextlist

    def generate_eqcl(self, obj, eqm):
        """ based on eqm and obj a list of equivalence classes
        with the object labels will be provided
        :var obj: original (full) list of objects
        :var eqm: result of method 'generate_equivalence_classes'
        :returns: eqcl -- list of equivalence classes
        """
        eqcl = []
        for i in range(0, len(eqm)):
            eqcl.append(0)
            eqcl[i] = []
            for i1 in range(0, len(eqm[i])):
                    eqcl[i].append(obj[eqm[i][i1]])
        return eqcl

    def _rename_double(self, names=[]):
        """rename if two names are identical

        :param list names: list of names
        :rtype: tuple
        :returns: unique_names - list inclusive renamed values
                  reneamed - list of old names, renamed
        """
        seen = set()
        unique_names = []
        counters = {}
        renamed = []
        for x in names:
            x = x.strip().replace(" ", "-")
            if x not in seen:
                seen.add(x)
                counters[x] = 0
                unique_names.append(x)
            else:
                counters[x] += 1
                renamed.append(x)
                unique_names.append('{}_{}'.format(x, counters[x]))
        return unique_names, renamed
