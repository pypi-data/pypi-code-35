import mimetypes
import random
import string


class MultipartEncoder:
    def __init__(self):
        self.fields = []
        self.files = []

    def add_file(self, field_name, path, encoding=None):
        with open(path, 'rb') as f:
            content = f.read()

        file_name = path.rsplit('/', 1)
        file_name = file_name[1] if len(file_name) == 2 else file_name[0]

        if encoding is None:
            encoding = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

        self.files.append((field_name, file_name, encoding, content))

    def add_field(self, name, value):
        self.fields.append((name, value))

    def encode(self):
        boundary = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        _boundary = b'--' + boundary.encode()

        parts = []

        for name, value in self.fields:
            parts.extend(
                [_boundary,
                 b'Content-Disposition: form-data; name="%s"' % name.encode(),
                 b'',
                 value.encode()
                 ]
            )

        for field_name, file_name, content_type, body in self.files:
            parts.extend(
                [_boundary,
                 b'Content-Disposition: form-data; name="%s"; filename="%s"' %
                 (field_name.encode(), file_name.encode()),
                 b'Content-Type: %s' % content_type.encode(),
                 b'',
                 body
                 ]
            )

        parts.append(_boundary + b'--')
        parts.append(b'')
        return boundary, b'\r\n'.join(parts)
