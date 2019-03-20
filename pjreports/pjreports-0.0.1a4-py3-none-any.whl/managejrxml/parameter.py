import warnings

class Parameter:
    """
    Parameter class manages jrxml parameter

    :Example:

    """

    def __init__(self, xml_node, namespaces = []):
        """
        Get an instance of a Parameter class given a xml_node
        :param xml_node:
        """
        # Initialize variables
        self.namespaces = namespaces;
        self.xml_node = xml_node
        self.name = None
        self.default_value = None
        self.value =  None
        self.java_class = None
        self.python_class = None
        # Parse xml node and get parameter name
        self._parse()

    def _parse(self):
        """

        :param xml_node:
        :return:
        """

        node_keys = self.xml_node.keys()
        if 'name' in node_keys:
            self.name = self.xml_node.attrib['name']
        if 'class' in node_keys:
            self.java_class = self.xml_node.attrib['class']
            self.python_class = self._map_java_class(self.java_class)

        # get parameter default value
        default_value_list = self.xml_node.findall('base:defaultValueExpression', self.namespaces)
        if len(default_value_list) > 0:
            value_node = default_value_list[0]
            self.default_value = value_node.text[1:-1]

    @staticmethod
    def _map_java_class(java_class):
        """

        :param java_class:
        :return: type
        """
        _type = 'unknown'
        if java_class == 'java.lang.String':
            _type = 'str'
        return _type

    def get_java_class(self):
        """

        :return:
        """
        return self.java_class

    def get_python_class(self):
        """

        :return:
        """
        return self.python_class


    def get_name(self):
        """

        :return:
        """
        return self.name

    def get_default_value(self):
        """

        :return:
        """
        return self.default_value

    def get_value(self):
        """

        :return:
        """
        return self.value

    def set_value(self, value):
        """

        :param value:
        :return:
        """
        # TODO validate value
        if type(value).__name__ == self.python_class:
            self.value = value
        else:
            warn = ('WARNING wrong parameter type for %s. User type is %s '
                    'while parameter type is %s') % (self.get_name(),type(value).__name__,self.get_python_class())
            warnings.warn(warn, UserWarning)




