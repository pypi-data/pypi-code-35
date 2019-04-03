class DataGetter:
    """ The data is wrapped inside data_object.DataGetter and accessible through get function.
       Methods:
           get: return the actual data. (In case of Lazy Data, this trigger the necessary calls to get the data)
    """
    def __init__(self, data):
        self.data = data

    def get(self):
        """
        :return:
            the actual data.
        """
        return self.data


