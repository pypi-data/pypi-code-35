import base64
import binascii
import json
import os

from .pades_measurement_units import PadesMeasurementUnits
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class PdfMarker(PkiExpressOperator):

    def __init__(self, config=PkiExpressConfig()):
        super(PdfMarker, self).__init__(config)
        self.__measurement_units = PadesMeasurementUnits.CENTIMETERS
        self.__page_optimization = None
        self.__marks = []
        self.__file_path = None
        self.__output_file_path = None
        self.__overwrite_original_file = False

    @property
    def file_path(self):
        return self.__file_path

    # region set_file

    def set_file_from_path(self, path):
        """

        Sets the file to be marked from its path.
        :param path: The path of the file to be marked.

        """
        if not os.path.exists(path):
            raise Exception('The provided file to be marked was not found')
        self.__file_path = path

    def set_file_from_raw(self, content_raw):
        """

        Sets the file to be marked from its content.
        :param content_raw: The content of the file to be marked.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__file_path = temp_file_path

    def set_file_from_base64(self, content_base64):
        """

        Sets the file to be marked from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the file to be
                               marked.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided file to be marked is not '
                            'Base64-encoded')
        self.set_file_from_raw(raw)

    # endregion

    @property
    def output_file(self):
        return self.__output_file_path

    @output_file.setter
    def output_file(self, value):
        self.__output_file_path = value

    @property
    def measurement_units(self):
        return self.__measurement_units

    @measurement_units.setter
    def measurement_units(self, value):
        self.__measurement_units = value

    @property
    def page_optimization(self):
        return self.__page_optimization

    @page_optimization.setter
    def page_optimization(self, value):
        self.__page_optimization = value

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        self.__marks = value

    @property
    def overwrite_original_file(self):
        return self.__overwrite_original_file

    @overwrite_original_file.setter
    def overwrite_original_file(self, value):
        self.__overwrite_original_file = value

    def apply(self):

        if self.__file_path is None:
            raise Exception('The file to be marked was not set')

        args = [self.__file_path]

        # Generate changes file.
        request = {
            'marks': [m.to_model() for m in self.__marks],
            'measurementUnits': self.__measurement_units,
            'pageOptimization': self.__page_optimization
        }
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(json.dumps(request).encode('ascii'))
        args.append(temp_file_path)

        # Logic to overwrite original file or use the output file.
        if self.__overwrite_original_file:
            args.append('--overwrite')
        else:
            args.append(self.__output_file_path)

        # This operation can only be used on versions greater than 1.3 of the
        # PKI Express.
        self._version_manager.require_version('1.3')

        # Invoke command.
        self._invoke(self.COMMAND_EDIT_PDF, args)


__all__ = ['PdfMarker']
