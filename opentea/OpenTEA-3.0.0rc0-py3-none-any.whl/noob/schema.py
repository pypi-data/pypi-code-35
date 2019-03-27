"""blahblah blah"""
from opentea.noob.noob import (nob_get, nob_find)


def load_default_meta(schema):
    """Load default values from a json-like schema

    Inputs:
    -----------
    schema : dictionary compatible with json-schema

    Return:
    -------
    default : A nested object filled with schema default values
    """
    paths = nob_find(schema, 'default')
    for i, _ in enumerate(paths, 0):
        paths[i] = clean_schema_addresses(paths[i], udf_stages=['default'])
    paths, ignored_indexes = _flatten_addresses(paths)

    values = []
    for path in paths:
        values.append(nob_get(schema, *path, 'default'))

    default = dict()
    for i, path in enumerate(paths, 0):
        _set_path_value(default, path, values[i])
    return default


def clean_schema_addresses(list_, udf_stages=None):
    """Clean a address from the addtitionnal layers of SCHEMA.

    Used only when a SCHEMA address must be found in the data to validate

     Parameters :
    -----------
    list_ : a list of string
        address in a nested dict
    udf_stages : a list of additionnal user defined stages (udf)
    Returns :
    ---------
    list
        the same list without SCHEMA intermedaite stages
    """
    skipped_stages = ["properties", "oneOf"]
    if udf_stages is not None:
        for udf_stage in udf_stages:
            skipped_stages.append(udf_stage)
    out = []
    for item in list_:
        if item not in skipped_stages:
            out.append(item)
    return out


def nob_complete(schema, obj_=None, dummy_items=False):
    """Completing nested object fill up on the basis
    of default reference values given by a schema

    Inputs:
    ----------
    schema : a json-schema like dictionnary
    obj_ : the nested object to be completed
    dummy_items : if True and arrays are empty, appends dummy items

    Returns :
    ---------
    the updated nested object
    """
    if obj_ is None:
        obj_ = dict()
    data_obj = obj_.copy()

    default = load_default_meta(schema)
    data_obj = _auto_fill(data_obj, default, dummy_items=dummy_items)
    return data_obj


def _flatten_addresses(addresses):
    """Falatten a nested object adressses and remove redundent
    elements

    Inputs:
    -----------
    adresses : a list of adresses (each address is a list of keys)

    Return:
    -------
    out : A list of cleaned adresses
    ignored_indexes : indexes corresponding to removed items
    """

    ignored_indexes = []
    for i, addr in enumerate(addresses, 0):
        for j, addr2 in enumerate(addresses, 0):
            if i != j:
                intersection = _lists_intersection(addr, addr2)
                if intersection and len(addr) == len(intersection):
                    ignored_indexes.append(i)
    ignored_indexes = list(set(ignored_indexes))
    ignored_indexes.sort()
    out = []
    for i, addr in enumerate(addresses, 0):
        if i not in ignored_indexes:
            out.append(addr)
    return out, ignored_indexes


def _set_path_value(nob, path, value=None):
    """Set value on a nob node or leaf

    Inputs:
    -----------
    nob :  a nested object
    path : address , a list of keys to the node/leaf
    value : the value contained by the node/leaf

    Return:
    -------
    nob : the updated nested object with the new node/leaf value
    """
    current = path[0]

    if len(path) > 1:

        next_ = path[1]
        index = 1
        current_type = 'dict'

        if isinstance(next_, int) or next_ == 'items':
            index = 2
            if isinstance(next_, int):
                current_type = 'Choice'
            else:
                current_type = 'Array'
        keys = _get_keys(nob)
        if current not in keys:
            nob = _append_node(nob, current, current_type)
        sub_nob = _nob_get_child(nob, current)
        if sub_nob is None:
            nob[current] = _init_type(current_type)
            sub_nob = _nob_get_child(nob, current)

        if isinstance(sub_nob, _OTChoice):
            if next_ == 0 and sub_nob.default is None:
                sub_nob.default = path[2]

        _set_path_value(sub_nob, path[index:], value=value)

    else:
        _set_leaf(nob, current, value)

    return nob


def _auto_fill(nob, ref, dummy_items=False):
    """auto fill a nested object with values
    from a reference nested object

    Inputs:
    ----------
    nob : a nested object
    ref : the reference nested object
    dummy_items : if True and the arrays are empty,
                 appends dummy items to the corresponding arrays

    Returns :
    ---------
    the updated nested object
    """
    ref_children = _get_keys(ref)
    inp_children = _get_keys(nob)

    for element_id in ref_children:
        child = _nob_get_child(ref, element_id)
        element_type = _get_type_name(child)
        if element_id in inp_children:
            inp_child = _nob_get_child(nob, element_id)
            type_inp_element = _get_type_name(inp_child)
            if type_inp_element != element_type:
                if not isinstance(child, (_OTChoice, _OTArray)):
                    _cut_leaf(nob, element_id)
                    _set_leaf(nob, element_id, child)
                else:
                    _handle_special(nob, ref, element_id,
                                    exists=True,
                                    dummy_items=dummy_items)
            else:
                _auto_fill(inp_child, child, dummy_items)
        else:

            if element_type not in ['_OTChoice', '_OTArray']:
                if element_type not in ['list', 'dict']:
                    _set_leaf(nob, element_id, child)
                else:
                    _append_node(nob, element_id, element_type)
                inp_child = _nob_get_child(nob, element_id)
                _auto_fill(inp_child, child, dummy_items)
            else:
                _handle_special(nob, ref, element_id,
                                exists=False,
                                dummy_items=dummy_items)

    junk_elements = _lists_difference(inp_children, ref_children)
    if junk_elements:
        for element_id in junk_elements:
            _cut_leaf(nob, element_id)
    return nob

class _OTArray(dict):
    """ OT array dictionnary
        the purpose of this class is to provide a way to distinguish
        dictionaries describing an opentea array from dictionaries used
        for other purposes
    """
    def __init__(self):
        """Startup class.
        """
        super().__init__(self)
        self['name'] = ''
        self._counter = 0

    def auto_name(self):
        """Generation of array item name if not provided
           in respect to the format 'Array Item X'
        """
        self._counter += 1
        return 'Array Item %d' % self._counter


class _OTChoice(dict):
    """ OT choice dictionnary
        the purpose of this class is to provide a way to distinguish
        dictionaries describing an opentea choice (XOR) from dictionaries used
        for other purposes
    """
    def __init__(self):
        """Startup class.
           the "default" attribute stores the default value
           of the choice
        """
        super().__init__(self)
        self.default = None


def _get_index(list_, list_item):
    """Get item index from a list of dictionnaries
    if the dictionnary contains the keyword "name"
    the corresponding dictionnary index in the list
    is returned. Otherwise return the index of the
    dictionnary containing the first occurence of
    the provided keyword

    Inputs :
    --------
    list_ :  a list of dictionnaries
    list_item :  the lookup keyword

    Outputs :
    --------
    index : index of the lookup dictionnary
    """
    for i, item in enumerate(list_, 0):
        keys = _get_keys(item)
        if 'name' in keys:
            if list_[i]['name'] == list_item:
                index = i
        else:
            if list_item in keys:
                index = i
                break
    return index


def _get_list_keys(nob):
    """Get the keys of the dictionnaries contained
    by a list

    Inputs :
    --------
    nob :  a list of dictionnaries

    Outputs :
    --------
    keys_list : a list of the dictionnaries keys
    """
    keys_list = []
    for item in nob:
        keys_list.extend(list(item.keys()))
    return keys_list


def _get_keys(nob):
    """Get nested object items

    Inputs :
    --------
    nob :  a nested object (could be a dict or a list of dicts)

    Outputs :
    --------
    keys_list : a list of the nested object items
    """
    if isinstance(nob, dict):
        keys_list = nob.keys()
    elif isinstance(nob, list):
        keys_list = _get_list_keys(nob)
    else:
        keys_list = []
    return keys_list

def _get_type_name(variable):
    """ get the type name of a variable

    Inputs:
    -----------
    variable : a python variable/class instance

    Return:
    -------
    type_ : A string describing the type or the class name of the variable
    """
    type_ = variable.__class__.__name__
    return type_

def _get_list_child(nob, child_id):
    """Extract an item from a nested object (list of dicts)

    Inputs:
    -----------
    nob :  a nested object (a list of dicts)
    child_id : the identifier of the item

    Return:
    -------
    child_nob : the corresponding item
    """
    index = _get_index(nob, child_id)
    child_nob = nob[index]
    return child_nob


def _init_type(item):
    """Generate a default type instances corresponding
    to a type provided as a string

    Inputs :
    --------
    item :  a string describing the type

    Outputs :
    --------
    kws_values[item] : an instance of the corresponding type
    """
    kws_values = {}
    kws_values['dict'] = dict()
    kws_values['list'] = []
    kws_values['Array'] = _OTArray()
    kws_values['Choice'] = _OTChoice()
    kws_values['NoneType'] = None
    return kws_values[item]


def _append_node(nob, item, item_type):
    """Append an item to a nested object

    Inputs :
    --------
    nob :  a nested object
    item :  the item identifier (string)
    item_type : the item type identifier
                (dict, list, Array, Choice or None)

    Outputs :
    --------
    nob : the provided nested object containing the appended item
    """
    nob = _set_leaf(nob, item, _init_type(item_type))
    return nob


def _set_leaf(nob, leaf, leaf_value):
    """Append a leaf to a nested object

    Inputs :
    --------
    nob :  a nested object
    leaf :  the leaf identifier (string)
    leaf_value : the value contained by the leaf

    Outputs :
    --------
    nob : the provided nested object containing the appended leaf
    """
    if isinstance(nob, dict):
        nob[leaf] = leaf_value
    elif isinstance(nob, list):
        keys = _get_keys(nob)
        if leaf in keys:
            child = _get_list_child(nob, leaf)
            child[leaf] = leaf_value
        else:
            nob.append({leaf: leaf_value})
    return nob


def _lists_difference(list_1, list_2):
    """Find elements which are in list_1 and not in list_2

    Inputs:
    -----------
    list_1 : list
    list_2 : list

    Return:
    -------
    diff : A list of elements which are in list_1 and not in list_2
    """

    diff = list(set(list_1) - set(list_2))
    return diff


def _lists_intersection(list_1, list_2):
    """Find elements which are in both list_1 andlist_2

    Inputs:
    -----------
    list_1 : list
    list_2 : list

    Return:
    -------
    inter : A list of elements which are in both list_1 and list_2
    """

    inter = list(set(list_1) & set(list_2))
    return inter


def _get_list_child(nob, child_id):
    """Extract an item from a nested object (list of dicts)

    Inputs:
    -----------
    nob :  a nested object (a list of dicts)
    child_id : the identifier of the item

    Return:
    -------
    child_nob : the corresponding item
    """
    index = _get_index(nob, child_id)
    child_nob = nob[index]
    return child_nob


def _nob_get_child(nob, child_id):
    """Extract an item from a nested object

    Inputs:
    -----------
    nob :  a nested object
    child_id : the identifier of the item

    Return:
    -------
    child_nob : the corresponding item
    """
    if isinstance(nob, dict):
        child_nob = nob[child_id]
    elif isinstance(nob, list):
        child_nob = _get_list_child(nob, child_id)
        if 'name' in child_nob:
            if child_nob['name'] != child_id:
                child_nob = child_nob[child_id]
        else:
            child_nob = child_nob[child_id]
    return child_nob


def _cut_leaf(nob, leaf):
    """Remove leaf from nob

    Inputs:
    -----------
    nob : a nested object
    leaf : key identifier for the leaf

    Return:
    -------
    nob : the updated nested object""

    """
    children = _get_keys(nob)
    if leaf not in children:
        print('%s is not a child of nob, try with one of those:\n' %leaf)
        print(children)
        raise Exception
    else:
        if isinstance(nob, dict):
            del nob[leaf]
        elif isinstance(nob, list):
            for i, item in enumerate(nob, 0):
                key = list(item.keys())[0]
                if key == leaf:
                    index = i
                    break
            del nob[index]
    return nob


def nob_flatten(obj_):
    """flatten a nested object.

    Parameters
    ----------
    obj_ : a nested object

    Returns :
    ---------
    out : list of addresses of objects contained in obj_
    """

    addresses = []

    def rec_walk(obj_, path):
        if isinstance(obj_, dict):
            for key in obj_:
                addresses.append(path + [key])
                rec_walk(obj_[key], path + [key])
        if isinstance(obj_, list):
            for key, item in enumerate(obj_):
                if isinstance(item, dict):
                    if "name" in item:
                        addresses.append(path + [key])
                rec_walk(item, path + [key])

    rec_walk(obj_, [])
    out, _ = _flatten_addresses(addresses)
    return out


def _handle_array(nob, ref, item_id, exists=False, dummy_items=False):
    """fill an array item of a nested object with values
    from a reference nested object

    Inputs:
    ----------
    nob : a nested object
    ref : the reference nested object
    item_id : the array item identifier
    exists : a boolean checking whether the item exists in the array
    dummy_items : if True and the array is empty, adds a dummy item

    Returns :
    ---------
    the updated nested object
    """

    ref_child = _nob_get_child(ref, item_id)
    if exists:
        inp_child = _nob_get_child(nob, item_id)
        if not isinstance(inp_child, list):
            _cut_leaf(nob, item_id)
            _append_node(nob, item_id, 'list')
            inp_child = _nob_get_child(nob, item_id)
        for item in inp_child:
            if not isinstance(item, dict):
                _cut_leaf(inp_child, item)
                _append_node(inp_child, item, 'dict')
    else:
        _append_node(nob, item_id, 'list')
        inp_child = _nob_get_child(nob, item_id)

    if not inp_child and dummy_items:
        inp_child.append(dict())

    inp_child = _nob_get_child(nob, item_id)
    for item in inp_child:
        if not 'name' in item:
            item['name'] = ref_child.auto_name()
        _auto_fill(item, ref_child, dummy_items)


def _handle_choice(nob, ref, item_id, exists=False, dummy_items=False):
    """fill a choice item of a nested object with values
    from a reference nested object

    Inputs:
    ----------
    nob : a nested object
    ref : the reference nested object
    item_id : the choice item identifier
    exists : a boolean checking whether the item exists in the array
    dummy_items : if True and no choice is provided,
                 sets the choice to default value

    Returns :
    ---------
    the updated nested object
    """
    ref_child = _nob_get_child(ref, item_id)
    choices = _get_keys(ref_child)
    default_choice = ref_child.default
    if exists:
        inp_child = _nob_get_child(nob, item_id)
        inp_choices = _get_keys(inp_child)
        if len(inp_choices) > 1 or not inp_choices:
            for item in inp_choices:
                _cut_leaf(inp_child, item)
            _set_leaf(inp_child, ref_child.default,
                      ref_child[ref_child.default])

        elif list(inp_choices)[0] not in choices:
            _cut_leaf(inp_child, list(inp_choices)[0])
            _set_leaf(inp_child, ref_child.default,
                      ref_child[ref_child.default])
        else:
            default_choice = list(inp_choices)[0]
    else:
        _append_node(nob, item_id, 'dict')
        inp_child = _nob_get_child(nob, item_id)
        _set_leaf(inp_child, ref_child.default,
                  ref_child[ref_child.default])
        _append_node(inp_child, default_choice, 'dict')

    inp_child = _nob_get_child(nob, item_id)
    _auto_fill(inp_child[default_choice],
               ref_child[default_choice],
               dummy_items)


def _handle_special(nob, ref, item_id, exists=False, dummy_items=False):
    """Handle special cases of array items and choice of a nested
    object that we want to auto-fill with valuesfrom a reference nested
    object

    Inputs:
    ----------
    nob : a nested object
    ref : the reference nested object
    item_id : the item identifier
    exists : a boolean checking whether the item exists
    dummy_items : if True and the array is empty, adds a dummy item

    Returns :
    ---------
    the updated nested object
    """
    child_ref = _nob_get_child(ref, item_id)
    if isinstance(child_ref, _OTArray):
        _handle_array(nob, ref, item_id,
                      exists=exists,
                      dummy_items=dummy_items)
    elif isinstance(child_ref, _OTChoice):
        _handle_choice(nob, ref, item_id,
                       exists=exists,
                       dummy_items=dummy_items)
