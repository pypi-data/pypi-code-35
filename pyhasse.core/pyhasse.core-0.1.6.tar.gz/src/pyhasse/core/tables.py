
class Field(object):
    """ a general table format for output

    :var title: Main title of the table
    :var subtitle: a more specifying title (can be empty)
    :var tdata: a matrix displaying the results (could also be only one column)
    :var hlabels: Labels of the rows (mostly the objects)
    :var: vlabels: Labels of the columns, problemspecific
    """

    def __init__(self, tdata=[], title=None, subtitle=None,
                 hlabels=True, vlabels=True, cssclass="",
                 transpose=False, placeholder="na"):
        self.title = title
        self.subtitle = subtitle
        self.tdata, \
            self.rows, \
            cols = self.convert_field2matrix(tdata,
                                             placeholder)
        self.hlabels = []
        self.vlabels = []
        if self.rows > 0:
            self.hlabels = self.tdata[0]
        if vlabels is None:
            self.tdata = tdata[1:]
        self.skip_hlabels = 0
        if hlabels is None:
            self.skip_hlabels = 1

    def convert_field2matrix(self, field, placeholder="na"):
        """Converts a field into a regular matrix structure
        :var field: input field with different lenghts of rows
        :var placeholder: to get a regular structure
                          not available data are filled with
                          placeholder"""
        lenField = len(field)
        maxLines = 0
        for i in range(0, lenField):
            if len(field[i]) >= maxLines:
                maxLines = len(field[i])
        matrix = []
        for i in range(0, lenField):
            matrix.append(0)
            matrix[i] = []
            for j in range(0, maxLines):
                if j < len(field[i]):
                    matrix[i].append(field[i][j])
                else:
                    matrix[i].append(placeholder)
        return matrix, lenField, maxLines

    def transpose_matrix(self, matrix):
        """ transposes (two-dimensional matrices
        :var r: number of rows of input matrix x
        :var k: number of columns  input matrix x
        :var matrix: input matrix  """

        matrixtr = []
        rows = len(matrix)
        cols = len(matrix[0])
        for j in range(0, cols):
            matrixtr.append(0)
            matrixtr[j] = []
            for i in range(0, rows):
                matrixtr[j].append(matrix[i][j])
        rowstr = cols
        colstr = rows
        return matrixtr, rowstr, colstr


class CSVTable(Field):
    """Convert field to csv data"""
    
    def table_as_csv(self):
        txt = []
        f1 = "{0},"
        f2 = "{0}\n"
        maxcol = len(self.hlabels)
        if self.title:
            txt.append(f2.format(self.title))
        if self.subtitle:
            txt.append(f2.format(self.subtitle))
        for i in range(0, len(self.tdata)):
            for j in range(self.skip_hlabels, maxcol-1):
                txt.append(f1.format(self.tdata[i][j]))
            txt.append(f2.format(self.tdata[i][maxcol-1]))
        return "".join(txt)


class HTMLTable(Field):
    """Exort field as html table"""

    def table2html(self):
        txt = []
        f2 = "{0}\n"
        table = "<table>{1}</table>"
        td = "<td>{0}</td>"
        tr = "<tr>{0}</tr>"
        cols = ""
        rows = []
        if self.title:
            txt.append(f2.format(self.title))
        if self.subtitle:
            txt.append(f2.format(self.subtitle))
        for i in range(0, len(self.tdata)):
            for j in range(self.skip_hlabels, len(self.hlabels)):
                cols += td.format(self.tdata[i][j])
            rows.append(tr.format(cols))
            cols = ""
        allrows = "".join(rows)
        return table.format("", allrows)

