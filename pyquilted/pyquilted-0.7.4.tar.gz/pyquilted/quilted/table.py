class Table:
    def __init__(self, cols=1, default=None):
        self.col_size = cols
        self.default = default
        self.rows = []

    def build(self, items):
        for row_start in range(0, len(items), self.col_size):
            col = self._column(items[row_start:row_start+self.col_size])
            self.rows.append(col.to_dict())
        return self.rows

    def _column(self, items):
        column = Columns(size=self.col_size, default=self.default)
        for item in items:
            column.add_item(item)
        return column


class Columns:
    def __init__(self, size=1, default=None):
        self.size = size
        self.default = default
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.size:
            self.items.append(item)

    def to_dict(self):
        columns = dict()
        columns['cols'] = self._fill_items()
        return columns

    def _fill_items(self):
        items_copy = self.items.copy()
        for i in range(len(items_copy), self.size):
            items_copy.append(self.default)
        return items_copy
