import copy

class DataDictionnary(dict):

    def get_keys(self):
        return [*self]

    def clear_none(self):
        for key, value in self.items():
            if value == None:
                self[key] = ""
                
    def update_default(self, new_dict):
        for key, value in new_dict.items():
            if key in self:
                self[key] = value
            else:
                print("Key {} cannot be found inside Default dictionnary".format(key))

    def get_copy(self):
        return copy.deepcopy(self)
