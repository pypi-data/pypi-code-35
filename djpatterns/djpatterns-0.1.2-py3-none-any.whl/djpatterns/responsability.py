class ResponsabilityBase(object):

    def __init__(self,next_class: 'Class' = None):
        """
        Construct of class  
        next_class: Class  
        """
        self.next = next_class

    def set_next(self,next_class: 'Class') -> None:
        """
        Setter next class of responsability  
        next_class: Class  
        """
        self.next = next_class

    def call_next(self,data: dict) -> None:
        """
        Call next resolver method  
        """
        self.next.resolver(data)

    def handle(self,data: dict) -> None:
        """
        Override this method for you make you validation. You must pass variables by date  
        data: Dict  
        """
        pass
    
    def resolver(self,data: dict = None) -> None:
        """
        Call handle and next handle of chain responsability if exist  
        data: Dict  
        return: None  
        """
        self.handle(data)
        if self.next:
            self.call_next(data)
        