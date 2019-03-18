import os
from urllib.parse import urlparse

from urllib3 import get_host


def url_query_convert_to_path(url, file_type):
    """Конвертация урла на path.
    Пример: http://lenta.ru/news/2013/03/dtp/index.html =>
            [CUR_DIR]/lenta.ru/news/2013/03/dtp/index.txt
    """
    host = get_host(url)[1]
    query = urlparse(url).path
    query = query.strip('/')
    query = '/'.join(query.split('/')[0:-1])
    file_name = list(filter(None, urlparse(url).path.split('/')))[-1]

    file_name = os.path.splitext(file_name)[0]
    return "{host}/{query}".format(host=host, query=query), \
           "{file_name}.{file_type}".format(
               file_name=file_name, file_type=file_type)

