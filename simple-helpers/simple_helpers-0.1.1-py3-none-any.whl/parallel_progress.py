from tqdm import tqdm
from multiprocessing import cpu_count
from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor

def parallel_progress(function, arguments, n_jobs=None):
    """
    Run an iterable of arguments through a function in
    parallel, returning an ordered list of results.

    Parameters
    ----------
    arguments:  array-like
        An iterable of the parameters being passed to function.
    function: function
        A python function to apply to the elements of array.
    n_jobs : int or NoneType, default None
        Number of cores to run jobs. If None is passed, then
        3/4 of the available processors will be used.
    
    Returns
    -------
    results : list
        List of returned objects from each application of function(arguments[i])
    """
    
    if n_jobs is None:
        n_jobs = int(0.75 * cpu_count())
    elif n_jobs==1:
        return [function(arg) for arg in tqdm(arguments)]

    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        futures = [pool.submit(function, arg) for arg in arguments]
        kwargs = {
            'desc': f"Processing {len(futures):,d} arguments through {repr(function).split(' ')[1]}",
            'total': len(futures),
            'unit': 'it',
            'unit_scale': True
        }
        for f in tqdm(as_completed(futures), **kwargs):
            pass
    results = [[]] * len(futures)
    for i, future in tqdm(enumerate(futures)):
        try:
            results[i] = future.result()
        except Exception as e:
            results[i] = e
    return results