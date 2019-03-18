from ..utils import make_cepnames

def write_cep(data):
    """
    Converts data matrix to the CEP compressed format.
    
    This function converts a data matrix from normal form, with species as rows 
    and samples as columns, to the Cornell Ecology Programs condensed format. 
    This condensed format consists of data ponts entered as couplets 
    consisting of the number for the species and the abundance. Each line of 
    the file begins with the number of the sample, followed by the couplets. 
    The data for a sample may continue onto other lines. See the user's manuals 
    for DECORANA and TWINSPAN for details on the structure of the CEP data files.

    Parameters
    ----------
    data : dataframe
        A pandas dataframe
    
    Returns
    -------
    rows: int
        number of rows in input dataframe
    columns : int
        number of columns in input dataframe

    Example
    --------
    import pandas as pd
    import cornpy as cp
    df = pd.read_csv("data.csv")
    rows, columns = cp.write_cep(df)
    """
    size = data.shape
    rows = size[0]
    columns = size[1]
    row_lab = data.index.tolist()
    col_lab = make_cepnames(data.columns)
    
    outfile = open("cep.dat", "w")

    title = 'dummy title\n'
    outfile.write(title)
    
    format = '(I3,5(I3,F3.0))\n'
    outfile.write(format)
    
    outfile.write("%3d \n" % 5)
    
    for i in range(rows):
        number_written = 0
        outfile.write("%3d" % (i+1))
        for j in range(columns):
            if data.iloc[i, j] != 0:
                outfile.write("%3d%3.0f" % ((j+1), data.iloc[i,j]))
                number_written += 1
                if number_written == 5:
                    outfile.write('\n')
                    outfile.write("%3d" % (i+1))
                    number_written = 0   
        if number_written != 0:
            outfile.write('\n')
    outfile.write("%3d \n" % 0)
     
    for j, m in enumerate(col_lab, 1):  
        outfile.write(m + ['', '\n'][j % 10 == 0])
    outfile.write('\n')
    for i, m in enumerate(row_lab, 1):  
        outfile.write(m.ljust(8) + ['', '\n'][i % 10 == 0])
 
    outfile.close()        
    return rows, columns