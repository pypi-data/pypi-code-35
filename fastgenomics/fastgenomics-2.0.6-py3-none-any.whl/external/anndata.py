try:
    import pandas as pd
    import numpy as np
    import scipy.sparse as sp
    from anndata import AnnData
except ImportError as e:
    msg = f"Could not import some of the necessary modules ({e.name}).  Please make sure to install anndata (https://github.com/theislab/anndata) with all its dependencies correctly (e.g. pandas, numpy, scipy)."
    raise ImportError(msg, name=e.name, path=e.path)
    raise e


GENE_METADATA_DTYPE = {"entrez_id": str}
CELL_METADATA_DTYPE = {"cell_id": str}
EXPRESSION_MATRIX_DTYPE = {
    "entrez_id": "category",
    "cell_id": "category",
    "expression": np.float64,
}


def check_file_type(file, content_type):
    """Returns a path if the file is of requested FASTGenomics type,
otherwise throws a TypeError."""
    if file.type != content_type:
        raise TypeError(
            f'File "{file.name}" is of type "{file.type}" but expected "{content_type}".'
        )


def read(expr, cell_meta=None, gene_meta=None):
    """Reads an anndata object by composing three files together:
`expression_matrix`, `cell_metadata` and `gene_metadata`."""
    check_file_type(expr, content_type="expression_matrix")
    expr = pd.read_csv(expr.path, dtype=EXPRESSION_MATRIX_DTYPE)

    obs = read_cell_metadata(cell_meta, expr)
    var = read_gene_metadata(gene_meta, expr)

    counts = read_sparse_matrix(expr, obs, var)

    adata = AnnData(counts, obs=obs, var=var, dtype="float64")
    return adata


def read_cell_metadata(cell_meta, expr):
    expr_cell_id = expr.cell_id.unique()

    if cell_meta is None:
        df = pd.DataFrame(data={"cell_id": expr_cell_id})
    else:
        check_file_type(cell_meta, content_type="cell_metadata")
        df = pd.read_csv(cell_meta.path, dtype=CELL_METADATA_DTYPE)

    df["cell_id"] = df["cell_id"].astype("category")
    df.set_index("cell_id", inplace=True)

    missing_ids = set(expr_cell_id) - set(df.index)
    if missing_ids:
        raise Exception(
            f'Some cell_id\'s were present in the expression matrix but not in "{cell_meta.path}": {missing_ids}.'
        )
    return df


def read_gene_metadata(gene_meta, expr):
    expr_entrez_id = expr.entrez_id.unique()

    if gene_meta is None:
        df = pd.DataFrame(data={"entrez_id": expr_entrez_id})
    else:
        check_file_type(gene_meta, content_type="gene_metadata")
        df = pd.read_csv(gene_meta.path, dtype=GENE_METADATA_DTYPE)

    df["entrez_id"] = df["entrez_id"].astype("category")
    df.set_index("entrez_id", inplace=True)

    missing_ids = set(expr_entrez_id) - set(df.index)
    if missing_ids:
        raise Exception(
            f'Some entrez_id\'s were present in the expression matrix but not in "{gene_meta.path}": {missing_ids}.'
        )

    return df


def read_sparse_matrix(expr, obs, var):
    cell_idx = pd.DataFrame(
        dict(cell_id=obs.index, cell_idx=np.arange(obs.shape[0]))
    ).set_index("cell_id")
    entrez_idx = pd.DataFrame(
        dict(entrez_id=var.index, entrez_idx=np.arange(var.shape[0]))
    ).set_index("entrez_id")
    expr = expr.merge(cell_idx, on="cell_id", copy=False)
    expr = expr.merge(entrez_idx, on="entrez_id", copy=False)

    counts = sp.coo_matrix(
        (expr.expression, (expr.cell_idx, expr.entrez_idx)),
        shape=(obs.shape[0], var.shape[0]),
    ).tocsr()

    return counts


# Writing
def write_exprs_csv(adata, csv_file):
    mat = adata.X.tocoo()
    df = pd.DataFrame.from_dict(
        dict(
            cell_id=adata.obs_names[mat.row],
            entrez_id=adata.var_names[mat.col],
            expression=mat.data,
        )
    )
    df.to_csv(csv_file, index=False)


def write(adata, expr=None, cell_meta=None, gene_meta=None):
    if expr is not None:
        check_file_type(expr, content_type="expression_matrix")
        write_exprs_csv(adata, expr.path)

    if cell_meta is not None:
        check_file_type(cell_meta, content_type="cell_metadata")
        adata.obs.to_csv(cell_meta.path)

    if gene_meta is not None:
        check_file_type(gene_meta, content_type="gene_metadata")
        adata.var.to_csv(gene_meta.path)
