
import xlrd
from contextlib import suppress


def convert(excel_file):
    for subclass in Converter.__subclasses__():
        converter = subclass(excel_file)

        return converter.convert()


class Converter:
    def __init__(self, excel_file):
        self._excel_file = excel_file
        self._file = xlrd.open_workbook(excel_file)

    def _get_columns(self, sheet_name, start=0):
        sheet = self._file.sheet_by_name(sheet_name)

        for colx in range(start, sheet.ncols):
            yield sheet.col_values(colx)

    def _get_capacities(self):
        raise NotImplementedError
    def _get_links(self):
        raise NotImplementedError

    def convert(self):
        network_request = {
            'capacities': self._get_capacities(),
            'links': self._get_links()
        }

        return network_request


class NewFormatConverter(Converter):
    def _get_columns(self, sheet_name, start=0):
        return super()._get_columns(sheet_name, start=1)

    def _get_capacities(self):
        capacities = []
        for column in self._get_columns('Capacities'):
            (name, units, item_type, options, lower_bound, upper_bound) = column

            capacity = {
                'name': name,
                'units': units,
                'type': item_type
            }

            if lower_bound != '' or upper_bound != '':
                capacity['bounds'] = {}

                with suppress(ValueError):
                    capacity['bounds']['lower'] = int(lower_bound)
                with suppress(ValueError):
                    capacity['bounds']['upper'] = int(upper_bound)

            capacities.append(capacity)

        return capacities

    def _get_links(self):
        links = []
        for column in self._get_columns('Network links'):
            (link_id, start_id, end_id, link_type, length, capacity, voltage, electrical_resistance,
             electrical_reactance, total_thermal_loss, total_pressure_loss, operating_temperature) = column

            link ={
                'id': int(link_id),
                'start_id': int(start_id),
                'end_id': int(end_id),
                'type': link_type,
                'length': length,
                'voltage': voltage,
                'resistance': electrical_resistance,
                'reactance': electrical_reactance,
                'total_thermal_loss': total_thermal_loss,
                'total_pressure_loss': total_pressure_loss,
                'operating_temp': operating_temperature,
            }

            try:
                capacity = float(capacity)
            except ValueError:
                capacity = str(capacity)

            link['capacity'] = capacity

            links.append(link)

        return links
