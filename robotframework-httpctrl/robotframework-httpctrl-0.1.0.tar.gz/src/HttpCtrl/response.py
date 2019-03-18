"""

HttpCtrl library provides HTTP/HTTPS client and server API to Robot Framework to make REST API testing easy.

Authors: Andrei Novikov
Date: 2018-2019
Copyright: GNU Public License

HttpCtrl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

HttpCtrl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

class Response:
    def __init__(self, status, body, headers):
        self.__status = status
        self.__body = body
        self.__headers = headers

    def __str__(self):
        if self.__body is None or len(self.__body) == 0:
            return str(self.__status)

        return "%s\n%s" % (str(self.__status), self.__body)

    def __copy__(self):
        return Response(self.__status, self.__body, self.__headers)

    def get_status(self):
        return self.__status

    def get_body(self):
        return self.__body

    def get_headers(self):
        return self.__headers
