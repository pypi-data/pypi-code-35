import pandas as pd
from operator import methodcaller

vector_funcs = {
        "between": "df.col.between",
        #case_when
        "coalesce": None,
        "cumall": "X",
        "cumany": "X",
        "cummean": "X",
        "desc": None,
        #"if_else",
        "lead": "shift(-1)",
        "lag": "shift(1)",
        "order_by": None,
        "n": "size",
        "n_distinct": None,
        "row_number": None,
        "min_rank": methodcaller("rank", method = "min"),
        "dense_rank": methodcaller("rank", method = "dense"),
        "percent_rank": None,
        "cume_dist": None,
        # plus tidyselect funcs
        }

unsupported = {
        "near": None,
        "nth": None,
        "first": None,
        "last": None,
        "ntile": None,
        "recode": None,
        "recode_factor": None,
        "na_if": None,
        }
