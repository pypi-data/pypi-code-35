from pyhasse.core.order import Order


class HDData(object):
    """show hasse diagram with D3

    :param string val: type of diagram (big|zoom)
    """

    def __init__(self, csv=None):
        self.csv = csv
        self.int_prec = 3
        self.dict = {}
        self.csv.calc_reduced_system()
        self.lrowsreduced = len(self.csv.objred)
        self.order = Order(self.csv.dmred,
                           self.csv.redrows,
                           self.csv.cols)

        # The matrix zeta describes comparabilities,
        # including transitive relations:
        # For example:  a < b and b < c then a < c
        # The transitive reduction of the zeta matrix: cover matrix.

        self.mx_zeta = self.order.calc_relatmatrix(datamatrix=self.csv.dmred,
                                                   rows=self.csv.redrows,
                                                   cols=self.csv.cols,
                                                   prec=int(self.int_prec))

        self.fd_levels_objs = self.order.calc_level(self.mx_zeta, csv.redrows)
        self.mx_coverdiagonal, \
            self.mx_cover = self.order.calc_cov(self.mx_zeta,
                                                self.csv.redrows)

        # get max objecs for all levels
        # to calculate distances in Hasse diagrams
        max = 0
        for level in self.fd_levels_objs:
            max = (max, len(level))[len(level) > max]

        # The Cover matrix is -so to say- the zeta ,
        # without transitive relations.
        self.dict['mx_cover'] = self.mx_cover
        # mx_zeta is used to calc the connections
        self.dict['mx_zeta'] = self.mx_zeta
        self.dict['mx_obj_red'] = self.csv.dmred
        self.dict['lst_obj_red'] = self.csv.objred
        self.dict['int_levels'] = len(self.fd_levels_objs)
        self.dict['fd_levels'] = self.fd_levels_objs
        self.dict['int_max_objs'] = max
        self.dict['mx_eq_classses'] = self.get_eq_objects()
        self.dict['lst_connections'] = self.get_connections()

    def jsondata(self):
        return self.dict

    def get_downsets(self, obj):
        idx = self.dict['lst_obj_red'].index(obj)
        lst_downsets = self.order.calc_downset(self.mx_zeta,
                                               self.csv.redrows)[idx]
        preselect = [self.csv.objred[i] for i in lst_downsets]
        return preselect

    def get_downset_connections(self, obj):
        lst_representants = []
        for i in range(0, len(self.csv.eqm)):
            lst_representants.append(self.csv.obj[self.csv.eqm[i][0]])
        print(80 * "#")
        print(lst_representants)

        connections = ""
        template = "{} -- {}, "

        lst_downsets = self.get_downsets(obj)
        print(80 * "+")
        print(lst_downsets)
        print(self.dict['mx_zeta'])
        for idxrow, row in enumerate(self.dict['mx_zeta']):
            obj_above = lst_representants[idxrow]
            for idxcol, col in enumerate(row):
                if row[idxcol] == 1:
                    obj_below = lst_representants[idxcol]
                    if obj_below != obj_above:
                        connections += template.format(obj_above, obj_below)
        return connections

    def get_upsets(self, obj):
        idx = self.dict['lst_obj_red'].index(obj)
        lst_upsets = self.order.calc_upset(self.mx_zeta,
                                           self.csv.redrows)[idx]
        lst_preselect = [self.csv.objred[i] for i in lst_upsets]
        return lst_preselect

    def get_incomparables(self, obj):
        idx = self.dict['lst_obj_red'].index(obj)
        lst_incomparables = self.order.calc_incompset(self.mx_zeta,
                                                      self.csv.redrows)[idx]
        lst_preselect = [self.csv.objred[i] for i in lst_incomparables]
        return lst_preselect

    def get_connections(self):
        """
        The cover matrix is the basis to construct a Hasse diagram, by stepwise
        arranging the conncections:

        Read for each row of the cover matrix ...
        ... the object name
        ... search in the correponding row the entry 1
        ... identify the column and its object name,
        ... draw this object name about that from where you are starting.
        ... connenct them.
        ... the object labels (names) correspond to the rows
        ... of dmred (dmobjred).


                     Full

                        d
                        |
                        c
                       / \
                      a   b
                       \ /
                        e
        """
        lst_connections = []
        for idxrow, row in enumerate(self.mx_cover):
            obj_above = self.csv.objred[idxrow]
            for idxcol, col in enumerate(row):
                if row[idxcol] == 1:
                    obj_below = self.csv.objred[idxcol]
                    lst_connections.append((obj_above, obj_below))
        return lst_connections

    def get_eq_objects(self):
        mx_eqclasses = {}
        for row in self.csv.eqm:
            mx_eqclasses[self.csv.obj[row[0]]] = []
            for val in row[1:]:
                mx_eqclasses[self.csv.obj[row[0]]].append(self.csv.obj[val])
        return mx_eqclasses
