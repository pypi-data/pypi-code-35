import inspect


def filter_dict(dict_to_filter, target_function,check_for_kwargs=True):
    sig = inspect.signature(target_function)
    if check_for_kwargs:
        if len([param.name for param in sig.parameters.values() if param.kind == param.VAR_KEYWORD])>0:
            return dict_to_filter
    filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
    filtered_dict = {filter_key: dict_to_filter[filter_key] for filter_key in filter_keys if filter_key in dict_to_filter}
    return filtered_dict

if __name__ == "__main__":
    def f(a,b=None,**kwargs):
        pass

    print(filter_dict({
        'a':0,
        'b':1,
        'c':2
    },f))
