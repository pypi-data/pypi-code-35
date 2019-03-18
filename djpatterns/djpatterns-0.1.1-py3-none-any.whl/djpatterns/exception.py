class ValidationChainException(Exception):
    """ Exception for errors in validate chain """
    
    def __init__(self,*args, **kwargs):
        """
        sobreescreve o metodo do init 
        """
        super().__init__(*args,**kwargs)