
def __get_dict_version(object, fields=None):
    var_dict = vars(object)
    prefix = '_{0}__'.format(object.__class__.__name__)
    new_dict = {}
    for k in var_dict.keys():
        new_k = k.replace(prefix, '')
        if fields == None or new_k in fields:
            if var_dict[k].__class__.__name__ == 'list':
                new_dict[new_k] = [__get_dict_version(o) for o in var_dict[k]]
            else:
                new_dict[new_k] = var_dict[k]
    return new_dict


def marshalling(db, experience):

    collection = db[experience.name]

    collection.insert_one(__get_dict_version(experience, ['name', 'attribute_map']))

    for s in experience.snapshots:
        collection.insert_one(__get_dict_version(s))

