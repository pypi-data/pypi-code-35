from multiprocess import Multiprocess

def multiprocess(fn, arr_of_args, **kwargs):
  """Execute several tasks in parallel. Requires a function `fn`
  and an array of argument tuples `arr_of_args`, each representing a call to the function.

  Additionally, you can provide arguments the same as you would with `Multiprocess`

  Example

    >>> # exec f(x) and f(y) in parallel
    >>> multiprocess(f, [(x,), (y,)])

  If you don't want a loading bar

    >>> multiprocess(f, [(x,), (y,)], show_loading_bar=False)
  """
  m = Multiprocess(**kwargs)
  m.add_tasks(fn, arr_of_args)
  m.do_tasks()
  m.close()
