import os
import tempfile
from pyasp.asp import *

def get_scopes(instance_f, encoding):
    """Get metabolic scope of a microbiota
    
    Args:
        instance_f (str): ASP instance file
        encoding (str): ASP model encoding
    
    Returns:
        TermSet: ASP model
    """
    prg = [encoding, instance_f]
    options = ''
    solver = Gringo4Clasp(clasp_options=options)
    models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    return models[0]


def get_grounded_communities(instance, encoding):
    """Ground the model, from a TermSet
    
    Args:
        instance (TermSet): model
        encoding (str): ASP model encoding
    
    Returns:
        bytes: grounded model
    """
    instance_f = instance.to_file()
    # print(os.path.abspath(instance_f))
    prg = [encoding, instance_f]
    grounder = Gringo4()
    grounding = grounder.run(prg)
    os.unlink(instance_f)
    return grounding

def get_grounded_communities_from_file(instance_f, encoding):
    """Ground the model, from a file
    
    Args:
        instance_f (str): model file
        encoding (str): ASP model encoding
    
    Returns:
        bytes: grounded model
    """
    prg = [encoding, instance_f]
    grounder = Gringo4()
    grounding = grounder.run(prg)
    # os.unlink(instance_f)
    return grounding

def get_communities_from_g(grounding):
    """Get optimal community, from grounding
    
    Args:
        grounding (bytes): grounded model
    
    Returns:
        TermSet: solution
    """
    options = '--configuration jumpy --opt-strategy=usc,5'
    solver = Clasp(clasp_options=options)
    models = solver.run(grounding,collapseTerms=True,collapseAtoms=False)
    return models[0]

def get_communities(lp_instance, encoding):
    """Get optimial community, from TermSet
    
    Args:
        lp_instance (TermSet): microbiota model
        encoding (str): ASP model encoding
    
    Returns:
        TermSet: solution
    """
    lp_f = lp_instance.to_file()
    prg = [encoding, lp_f]
    print(os.path.abspath(lp_f))
    options = '--configuration jumpy --opt-strategy=usc,5'
    solver = Gringo4Clasp(clasp_options=options)
    models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    os.unlink(lp_f)
    # print(models[0])
    return models[0]

def get_intersection_communities_from_g(grounding, optimum):
    """Get intersection of solutions, from grounding
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
    
    Returns:
        TermSet: intersection
    """
    options = '--configuration jumpy --opt-strategy=usc,5 --enum-mode cautious --opt-mode=optN --opt-bound=' +str(optimum)
    solver = Clasp(clasp_options=options)
    intersec = solver.run(grounding,collapseTerms=True,collapseAtoms=False)
    return intersec[0]

def get_intersection_communities_from_g_noopti(grounding):
    """Get intersection of solutions, from grounding, without optimal score
    
    Args:
        grounding (bytes): grounded model
    
    Returns:
        TermSet: intersection
    """
    options = '--configuration jumpy --opt-strategy=usc,5 --enum-mode cautious --opt-mode=optN'
    solver = Clasp(clasp_options=options)
    intersec = solver.run(grounding,collapseTerms=True,collapseAtoms=False)
    return intersec[0]

def get_intersection_communities(lp_instance, optimum, encoding):
    """Get intersection of solutions, from TermSet
    
    Args:
        lp_instance (TermSet): microbiota model
        optimum (str): optimal score
        encoding (str): ASP model encoding
    
    Returns:
        TermSet: intersection
    """
    lp_f = lp_instance.to_file()
    prg = [encoding, lp_f]
    options = '--configuration jumpy --opt-strategy=usc,5 --enum-mode cautious --opt-mode=optN --opt-bound=' +str(optimum)
    solver = Gringo4Clasp(clasp_options=options)
    intersec = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    os.unlink(lp_f)
    return intersec[0]

def get_all_communities_from_g(grounding, optimum, nmodels=0):
    """Get all optimal communities, from grounding
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
        nmodels (int, optional): Defaults to 0. number of models to compute, 0 = all
    
    Returns:
        list: list of Termsets
    """
    options = str(nmodels)+' --configuration handy --opt-strategy=usc,5 --opt-mode=optN --opt-bound=' +str(optimum)
    solver = Clasp(clasp_options=options)
    models = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return models

def get_all_communities_from_g_noopti(grounding, nmodels=0):
    """Get all optimal communities, from grounding, without optimal score
    
    Args:
        grounding (bytes): grounded model
        nmodels (int, optional): Defaults to 0. number of models, 0 = all
    
    Returns:
        list: list of TermSets
    """
    options = str(nmodels)+' --configuration handy --opt-strategy=usc,5 --opt-mode=optN '
    solver = Clasp(clasp_options=options)
    models = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return models

def get_all_communities(lp_instance, optimum, encoding, nmodels=0):
    """Get all communities, from TermSet
    
    Args:
        lp_instance (TermSet): microbiota model
        optimum (str): optimal score
        encoding (str): ASP model encoding file
        nmodels (int, optional): Defaults to 0. number of models, 0 = all
    
    Returns:
        list: list of TermSets
    """
    lp_f = lp_instance.to_file()
    prg = [encoding, lp_f]
    options = str(nmodels)+' --configuration handy --opt-strategy=usc,5 --opt-mode=optN --opt-bound=' +str(optimum)
    solver = Gringo4Clasp(clasp_options=options)
    models = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(lp_f)
    return models

def get_union_communities_from_g(grounding, optimum):
    """Get union of all community solutions
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
    
    Returns:
        TermSet: union
    """
    options ='--configuration jumpy --opt-strategy=usc,5 --enum-mode=brave --opt-mode=optN --opt-bound='+str(optimum)
    solver = Clasp(clasp_options=options)
    union = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return union[0]

def get_union_communities_from_g_noopti(grounding):
    """Get union of all community solutions, from grounding, without optimal score
    
    Args:
        grounding (bytes): grounded instance
    
    Returns:
        TermSet: union
    """
    options ='--configuration jumpy --opt-strategy=usc,5 --enum-mode brave --opt-mode=optN'
    solver = Clasp(clasp_options=options)
    union = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return union[0]

def get_union_communities(lp_instance, optimum, encoding):
    """Get union of community solutions, from TermSet
    
    Args:
        lp_instance (TermSet): microbiota model
        optimum (str): optimal score
        encoding (str): ASP encoding model file
    
    Returns:
        TermSet: union
    """
    lp_f = lp_instance.to_file()
    prg = [encoding, lp_f]
    options ='--configuration jumpy --opt-strategy=usc,5 --enum-mode=brave --opt-mode=optN --opt-bound='+str(optimum)
    solver = Gringo4Clasp(clasp_options=options)
    union = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(lp_f)
    return union[0]

def get_unproducible(draft, seeds, targets, encoding):
    """Get unproducible targets in a microbiota
    
    Args:
        draft (TermSet): metabolic model
        seeds (TermSet): seeds
        targets (TermSet): targets
        encoding (str): ASP model encoding
    
    Returns:
        TermSet: unproducible targets
    """
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    target_f = targets.to_file()
    prg = [encoding, draft_f, seed_f, target_f]
    solver = Gringo4Clasp()
    models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return models[0]

def get_transported(instance, encoding):
    """Get transported metabolites
    
    Args:
        instance (TermSet): microbiota model
        encoding (str): ASP model encoding
    
    Returns:
        TermSet: transported metabolites
    """
    instance_f = instance.to_file()
    prg = [encoding, instance_f]
    solver = Gringo4Clasp()
    models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    # print(os.path.abspath(instance_f))
    os.unlink(instance_f)
    return models[0]


def get_grounded_instance_exchanged_metabolites(instance, encoding, exchanged_in_escope=False):
    """Get grounding under compartmentalized framework
    
    Args:
        instance (TermSet): microbiota model
        encoding (str): ASP model encoding
        exchanged_in_escope (bool, default=False): additional option for ASP
    
    Returns:
        bytes: grounded model
    """
    instance_f = instance.to_file()
    if exchanged_in_escope:
        options = "--const exchanged_in_escope=1"
    else:
        options = "--const exchanged_in_escope=0"
    print(os.path.abspath(instance_f))
    prg = [encoding, instance_f]
    grounder = Gringo4(gringo_options=options)
    grounding = grounder.run(prg)
    os.unlink(instance_f)
    return grounding

def get_grounded_instance_exchanged_metabolites_from_file(instance_f, encoding, exchanged_in_escope=False):
    """Get grounding from file
    
    Args:
        instance_f (str): microbiota model file
        encoding (str): ASP model encoding
        exchanged_in_escope (bool, default=False): additional ASP option
    
    Returns:
        bytes: grounded model
    """
    if exchanged_in_escope:
        options = "--const exchanged_in_escope=1"
    else:
        options = "--const exchanged_in_escope=0"
    print(os.path.abspath(instance_f))
    prg = [encoding, instance_f]
    grounder = Gringo4(gringo_options=options)
    grounding = grounder.run(prg)
    return grounding

def get_exchanged_metabolites_onesol(grounding):
    """Select community in compartmentalized framework
    
    Args:
        grounding (bytes): grounded model
    
    Returns:
        TermSet: solution
    """
    options = "--configuration=jumpy --opt-strategy=usc,5"
    solver = Clasp(clasp_options=options)
    models = solver.run(grounding,collapseTerms=True,collapseAtoms=False)
    return models

def get_exchanged_metabolites_intersection(grounding, optimum):
    """Get intersection of communities solutions
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
    
    Returns:
        TermSet: intersection
    """
    options='--configuration jumpy --opt-strategy=usc,5 --enum-mode cautious --opt-mode=optN --opt-bound='+str(optimum)
    solver = Clasp(clasp_options=options)
    intersec = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return intersec[0]

def get_exchanged_metabolites_allsol(grounding, optimum, nmodels=0):
    """Get all communities
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
        nmodels (int, optional): Defaults to 0. number of models, 0 = all
    
    Returns:
        Set: set of TermSets
    """
    options = str(nmodels)+' --configuration jumpy --opt-strategy=usc,5 --opt-mode=optN --opt-bound='+str(optimum)
    solver = Clasp(clasp_options=options)
    models = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return models

def get_exchanged_metabolites_union(grounding, optimum):
    """Get union of community solutions
    
    Args:
        grounding (bytes): grounded model
        optimum (str): optimal score
    
    Returns:
        TermSet: union
    """
    options ='--configuration jumpy --opt-strategy=usc,5 --enum-mode brave --opt-mode=optN --opt-bound='+str(optimum)
    solver = Clasp(clasp_options=options)
    union = solver.run(grounding, collapseTerms=True, collapseAtoms=False)
    return union[0]
