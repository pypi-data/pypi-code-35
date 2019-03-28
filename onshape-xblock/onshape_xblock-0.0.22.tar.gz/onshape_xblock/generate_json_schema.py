from serialize import Serialize

def get_check_fields():
    check_name_list = [{"type": "check_volume"},
                       {"type": "check_mass"},
                       {"type": "check_center_of_mass"},
                       {"type": "check_configuration"},
                       {"type": "check_base"}]
    check_class_list = Serialize.init_class_list(check_name_list, init_class=False)
    return check_class_list

if __name__ == "__main__":
    print get_check_fields()