def make_cepnames(names, seconditem=False):
    """
    Abbreviates a botanical or zoological Latin name into an eight-character 
    name.
    
    Cornell Ecology Programs (CEP) use eight-letter abbreviations for species 
    and site names. In species, the names are formed by taking four first 
    letters of the generic name and four first letters of the specific or 
    subspecific epithet. In this function, the CEP name is made by taking the 
    four first letters of the first element, and four first letters of the last 
    (default) or the second element (with seconditem=True). If there was only 
    one name element, it is abbreviated to eight letters. The returned names 
    are made unique by adding numbers to duplicate names. These names may be 
    practical to avoid congestion in ordination plots.

    Parameters
    ----------
    names : list
        a list of names to be formatted into CEP names
    seconditem : bool, optional
        Take always the second item of the original name to the 
        abbreviated name instead of the last original item (default is False).
    
    Returns
    -------
    cepnames : list
        a list of CEP names

    Example
    --------
    import cornpy as cp
    cepnames = cp.make_cepnames(["Aa maderoi", "Poa sp.", "Cladina rangiferina",
                    "Cladonia cornuta", "Cladonia cornuta var. groenlandica",
                    "Cladonia rangiformis", "Bryoerythrophyllum"])
    """
    count = 1
    cepnames = list()
    for name in names:
        n = len(name.split()) if not seconditem else 2
        str1 = name.split()[0]
        try:
            str2 = name.split()[n-1]
        except IndexError:
            str2 = str1
        cepstr = str1[0:4] + str2[0:4].rstrip('.') if str1 != str2 else str1[0:8]
        if not cepstr in cepnames:
            cepnames.append(cepstr)
        else:
            cepnames.append(cepstr[0:7] + str(count))
            count += 1
    return(cepnames)