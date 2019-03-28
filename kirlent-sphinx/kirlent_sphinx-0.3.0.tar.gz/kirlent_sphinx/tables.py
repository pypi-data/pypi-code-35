# Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>
#
# Derived from the cloud_sptheme.ext.table_styling project:
#   https://cloud-sptheme.readthedocs.io/
# Read the included LICENSE_cloud_spheme.txt file for details.

from itertools import zip_longest

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.patches import RSTTable


# =============================================================================
# field option parsers
# =============================================================================


def _split_argument_list(argument):
    if "," in argument:
        return argument.split(",")
    else:
        return argument.split()


def _parse_argument_map(argument, argmap, param):
    args = _split_argument_list(argument)
    if len(args) == 1 and all(c in argmap for c in args[0]):
        args = args[0]

    def norm(arg):
        try:
            return argmap[arg]
        except KeyError:
            raise ValueError("invalid %s: %r" % (param, arg))

    return [norm(arg) for arg in args]


_alignment_map = {
    "l": "left",
    "r": "right",
    "c": "center",
    "j": "justify",
    "left": "left",
    "right": "right",
    "center": "center",
    "centered": "center",
    "justify": "justify",
    "justified": "justify",
}


def alignment_list(argument):
    """convert into list of alignment options.
    raise ``ValueError`` if no args found, or invalid strings.
    """
    return _parse_argument_map(argument, _alignment_map, "alignment")


_bool_map = {
    "true": True,
    "t": True,
    "yes": True,
    "y": True,
    "false": False,
    "f": False,
    "no": False,
    "n": False,
}


def bool_list(argument):
    """convert to list of true/false values"""
    return _parse_argument_map(argument, _bool_map, "boolean value")


def class_option_list(argument):
    """convert to list of list of classes"""
    args = _split_argument_list(argument)
    return [directives.class_option(arg) for arg in args]


_divider_map = {
    "0": "no",
    "1": "single",
    "2": "double",
    "none": "no",
    "single": "single",
    "double": "double",
}


def divider_list(argument):
    return _parse_argument_map(argument, _divider_map, "divider style")


class ExtendedRSTTable(RSTTable):
    """A directive for generating tables with more details."""

    option_spec = RSTTable.option_spec.copy()
    option_spec.update(
        {
            "header-columns": directives.nonnegative_int,
            "widths": directives.positive_int_list,
            "column-alignment": alignment_list,
            "header-alignment": alignment_list,
            "column-wrapping": bool_list,
            "column-classes": class_option_list,
            "column-dividers": divider_list,
        }
    )

    def run(self):
        result = RSTTable.run(self)
        if result and isinstance(result[0], nodes.table):
            self._update_table_classes(result[0])
        return result

    def _update_table_classes(self, table):
        table_classes = table["classes"]
        table_classes.append("table")

        # figure out how many header rows & columns
        options = self.options
        header_cols = options.get("header-columns") or 0
        widths = options.get("widths")

        # Parse column options into list of ColumnOptions records.
        # If any option is short, it will be padded with ``None`` values
        # to match the longest list.
        EMPTY = ()
        opts = tuple(
            zip_longest(
                options.get("column-alignment", EMPTY),
                options.get("header-alignment", EMPTY),
                options.get("column-wrapping", EMPTY),
                options.get("column-classes", EMPTY),
                options.get("column-dividers", EMPTY),
            )
        )
        NULL_OPTIONS = [None] * 5

        # try to find "tgroup" node holding thead/tbody etc
        def locate(cls):
            for child in table.children:
                if isinstance(child, cls):
                    return child
            return None

        tgroup = locate(nodes.tgroup)
        if not tgroup:
            return

        # loop through content of 'tgroup' node --
        # should be 0+ 'colspec' nodes, 0-1 thead node, and 0-1 tbody nodes.
        # NOTE: using 'cgroup_idx' as hack to track colgroup index
        cgroup_idx = 0
        for child in tgroup:
            # handle colspec entry (corresponding to COLGROUP)
            # set group width & mark "header" columns
            if isinstance(child, nodes.colspec):
                if widths and cgroup_idx < len(widths):
                    child["colwidth"] = widths[cgroup_idx]
                if cgroup_idx < header_cols:
                    child["stub"] = 1
                cgroup_idx += 1
                continue

            # otherwise have thead / tbody --
            # loop through each row in child, adding classes as appropriate
            assert isinstance(child, (nodes.thead, nodes.tbody))
            for row in child.children:

                # check if we're in a header
                is_header_row = isinstance(child, nodes.thead)

                # Add alignment and wrap classes to each column (would add to
                # colspec instead, but html doesn't inherit much from colgroup)
                # We iterate trough the list of table cells in the row while
                # maintaining the column format index in parallel
                assert isinstance(row, nodes.row)
                colidx = 0  # visible idx, to account for colspans
                prev_col_classes = None
                for idx, col in enumerate(row):

                    # get align/wrap options for column
                    try:
                        col_opts = opts[colidx]
                    except IndexError:
                        col_opts = NULL_OPTIONS
                    align, header_align, wrap, clist, divider = col_opts

                    # let header values override defaults
                    if is_header_row:
                        align = header_align
                    if align is None:
                        align = "left"

                    # add alignment / wrapping classes for column
                    assert isinstance(col, nodes.entry)
                    classes = col["classes"]
                    if align:
                        classes.append("text-" + align)
                    if wrap is False:
                        classes.append("whitespace-no-wrap")
                    if clist:
                        classes.extend(clist)

                    if divider:
                        # add divider class for left side of this column,
                        classes.append(divider + "-left-divider")

                        # same divider type to right side of previous column,
                        # so that css can bind to either.
                        if prev_col_classes is not None:
                            prev_col_classes.append(divider + "-right-divider")

                    # update prev_col_classes for next pass
                    prev_col_classes = classes

                    # Now it's the time to advance the column format index.
                    # If we have a cell spans across the columns, we add the
                    # value of 'morecols', so we get the proper right divider
                    # for the current cell and the proper format index for the
                    # next loop iteration
                    colidx += 1 + col.get("morecols", 0)

                # add divider to right side of last column
                if prev_col_classes and colidx < len(opts):
                    align, header_align, wrap, clist, divider = opts[colidx]
                    if divider:
                        prev_col_classes.append(divider + "-right-divider")


def setup(app):
    """Add the directives to a Sphinx application."""
    directive_map = directives._directives
    if directive_map.get("table") is RSTTable:
        directive_map.pop("table")
    app.add_directive("table", ExtendedRSTTable)
