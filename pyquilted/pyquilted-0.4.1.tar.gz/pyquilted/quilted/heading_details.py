class HeadingDetails:
    """The heading section located at the top of a quilted resume

       A heading object to determine type of format to use. Heading is
       made up of details like objective, location, flair and title.
       It is semi-ordered in that title, location and flair can be in
       any order.
    """
    def __init__(self, name=None, an_objective=None, the_details=None,
                 **kwargs):
        self.name = name
        self.objective = an_objective
        self.details = the_details or []

    def add_detail(self, detail):
        self.details.append(detail.serialize())

    def set_name(self, name):
        self.name = name

    def set_objective(self, objective):
        self.objective = objective.serialize()
