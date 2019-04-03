from pprint import pprint


class ModelDeleter(object):

    def __init__(self, model_cls, selector_fields, keeper_fields):
        self.model_cls = model_cls
        self.selector_fields = selector_fields
        self.keeper_fields = keeper_fields

        self.reset()
    
    def reset(self):
        self.selectors = []
        self.keepers = []
    
    def collect_model(self, model):
        filters = self.__collect_filters(model, self.selector_fields)
        if filters not in self.selectors:
            self.selectors.append(filters)
            
        filters = self.__collect_filters(model, self.keeper_fields)
        if filters not in self.keepers:
            self.keepers.append(filters)

    def __collect_filters(self, model, fields):
        filters = {}
        for field in fields:
            if not hasattr(model, field):
                filters[field] = None
            else:
                filters[field] = getattr(model, field)
        return filters
    
    def execute_delete(self, adapter_cls, adapter_settings):
        adapter_cls.execute_delete(self.model_cls,
                                   self.selectors, self.keepers,
                                   adapter_settings)
        self.reset()
    
    def execute_unref(self, parent_model, fkey, adapter_cls, adapter_settings):
        adapter_cls.execute_unref(parent_model, fkey,
                                  self.selectors, self.keepers,
                                  adapter_settings)
        self.reset()
    
    def pprint(self):
        pprint({
            'selectors': self.selectors,
            'keepers': self.keepers,
            'selector_fields': self.selector_fields,
            'keeper_fields': self.keeper_fields,
        })
        
        