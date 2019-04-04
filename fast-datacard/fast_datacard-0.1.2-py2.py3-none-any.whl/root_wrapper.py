"""
    Wrapping all import that would access ROOT to make testing easier (for now)
"""


def Open(*args):
    import ROOT
    return ROOT.TFile.Open(*args)


def TH1F(*args):
    import ROOT
    return ROOT.TH1F(*args)


def array2hist(*args):
    from root_numpy import array2hist as orig
    orig(*args)


def Double(*args):
    import ROOT
    return ROOT.Double(*args)


def GetDirectory(*args):
    import ROOT
    return ROOT.gDirectory.GetDirectory(*args)


def GetPath():
    import ROOT
    return ROOT.gDirectory.GetPath()
