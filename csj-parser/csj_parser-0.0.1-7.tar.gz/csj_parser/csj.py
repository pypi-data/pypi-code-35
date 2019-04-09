import json


class Csj():

    def to_dict(csj_string: str) -> dict:
        """Convert csj string to list of dict"""
        csj_string = csj_string.strip()
        lines = csj_string.splitlines()
        return Csj.convert_csj_to_array_json(lines)


    def convert_csj_to_array_json(lines: list) -> list:
        result = []
        for line in lines[1:]:
            result.append(Csj.convert_csj_to_dict(lines[0], line))
        return result


    def convert_csj_to_dict(key: str, value: str) -> dict:
        """Convert string in CSJ format into dictionary."""
        header = json.loads(f'[{key}]')
        content = json.loads(f'[{value}]')
        return dict(zip(header, content))


    def from_dicts(list_of_dicts: list) -> str:
        csj_string = ','
        keys = list(list_of_dicts[0].keys())
        csj_string = csj_string.join('"{}"'.format(key) for key in keys)
        csj_string = csj_string + '\n'
        for d in list_of_dicts:
            values = json.dumps(list(d.values()), separators=(',',':'))[1:-1]
            csj_string = csj_string + values + '\n'
        return csj_string
