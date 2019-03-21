import os
import xml.etree.ElementTree as ET
from .managejrxml.parameter import Parameter
import warnings
from tabulate import tabulate
import tempfile
import subprocess
from .settings import config_box

class Report:
    """
    Manages jasperreports templates.
    his class allows:
        - jrxml properties inspection
        - set report parameters
        - print report using pjreports-java jar-
    Dependencies:
        - JAVA >= 1.7
    """

    def __init__(self, jrxml_template_path, name=""):
        """

        :param jrxml_template_path:
        :param name:
        """
        # Properties initialization
        self.name = ""
        self.template_path = ""
        self.parameters = []
        self.parameters_name = []
        self.namespaces = {'base': 'http://jasperreports.sourceforge.net/jasperreports'}
        self.add_template(name, jrxml_template_path)
        self._get_template_parameters()
        self.temp_file = None

    def add_template(self, name, jrxml_template_path):
        """

        :param jrxml_template_path:
        :param name:
        :return:
        """
        self.name = name
        self.template_path = jrxml_template_path

    def _get_template_parameters(self):
        """
        This method parses the jrxml template and searches the tag "parameter"
        Example:
        <parameter name="image1" class="java.lang.String" isForPrompting="false">
            <parameterDescription><![CDATA[Imagen 1]]></parameterDescription>
            <defaultValueExpression><![CDATA[java.lang.String("hola")]]></defaultValueExpression>
        </parameter>
        :return:
        """
        # Read the jrxml tempalte as a xml file
        et = ET.parse(self.template_path)
        root = et.getroot()
        # TODO manage namespaces better

        for parameter in root.findall('base:parameter', self.namespaces):
            # Parse parameter
            self.add_parameter(parameter)

    def add_parameter(self, parameter_xml_node):
        param = Parameter(parameter_xml_node, self.namespaces)
        self.parameters_name.append(param.get_name())
        self.parameters.append(param)

    def list_parameters(self):
        table = []
        for parameter in self.parameters:
            aux = [parameter.get_name(),
                   parameter.get_value(),
                   parameter.get_default_value(),
                   parameter.get_java_class(),
                   parameter.get_python_class()]
            table.append(aux)
        print(tabulate(table, headers=['Name', 'Value', 'Default_Value', 'java_class', 'python_class']))

    def set_parameter(self, parameter_name, parameter_value):
        # Get parameter reference
        if parameter_name not in self.parameters_name:
            warn = ('WARNING parameter %s not in parameters')%parameter_name
            warnings.warn(warn, UserWarning)
            return

        # Get parameter
        index = self.parameters_name.index(parameter_name)

        # Set parameter value
        self.parameters[index].set_value(parameter_value)


    def get_parameter_value(self, parameter_name):
        pass

    def _check_parameter(self, parameter_name, parameter_value):
        pass

    def add_text(self, name, value, target):
        """

        :param name:
        :param value:
        :param target:
        :return:
        """
        pass

    def add_image(self, name, value, target):
        """

        :param name:
        :param value:
        :param target:
        :return:
        """
        pass


    def print_report_as_pdf(self, folder, filename):

        # Crear carpeta para report si no existe

        # Crear archivo temporal de datos si no existe
        self._create_text_file_for_report()
        # Exportar
        path_to_java = os.path.join(config_box.DIRECTORIES.JAVA,'jpreports-java.jar')
        print(path_to_java)
        save_path = os.path.join(folder,filename)

        result = subprocess.run(['java','-jar',path_to_java,
                                 self.temp_file.name,
                                 self.template_path,
                                 save_path])
        print(result.stdout)
        return save_path
        # java -jar jpreports-java.jar jrxml datafile exportpath
        

    def _create_text_file_for_report(self):
        """

        :param folder:
        :return:
        """
        # Create temporary text file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'$parameters\n')
        for parameter in self.parameters:
            value = parameter.get_value()
            if value is None:
                value = parameter.get_default_value();
            if value is not None:
                aux = parameter.get_name() + ';' + value +'\n'
                self.temp_file.write(str.encode(aux))
        #Force dump to file
        self._close_temp_file_for_report()

    def _close_temp_file_for_report(self):
        self.temp_file.close()


    def _launch_jasper(self):
        pass