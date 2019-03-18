import requests
import logging
import os

from .workbook import Workbook

from .utils import sanitize_phone, verify_phone_format

from .errors import (
    InvalidTokenError, InvalidJSONResponseError, InvalidPhoneFormatError
)

from .constants import PROD_DNC_URL, MOCK_DNC_URL

log = logging.getLogger(__name__)


class RealValidation:
    """RealValidation Application Object

    Parameters
    ----------
    workbooks : list
        List of workbook paths to validate against RealValidation DNC API
    token : str
        RealValidation API Token. Defaults to environmental variable
        ``RV_TOKEN``
    output : str
        RealValidation API Output. Defaults to ``json``
    url : str
        RealValidation API URL. Defaults to
        ``https://api.realvalidation.com/rpvWebService/DNCLookup.php``
    phone_regex : str
        Regex to use when validating phone numbers. Defaults to ``r'^\d{10}$'``
    staging: bool
        If ``True`` RealValidation utilizes the Mock API, overrides ``url``
        parameter

    """

    workbooks = []

    def __init__(self,
                 url=PROD_DNC_URL,
                 token=os.environ.get('RV_TOKEN'),
                 output='json',
                 staging=False):

        if token is None:
            raise InvalidTokenError

        self.url = url
        self.token = token
        self.output = output

        if staging:
            self.url = MOCK_DNC_URL

        log.debug('<RealValidation {} >'.format(self.__dict__))

    def add_workbook(self, workbook_path):
        self.workbooks.append(Workbook(workbook_path))

    def lookup_phone(self, phone):
        """Makes a request to the RealValidation DNC API

        Parameters
        ----------
        phone : str
            10 numerical digits representing a phone number.

        Returns
        -------
        dict
            Dictionary representing JSON response from RealValidation DNC API.

        """
        # remove any non-numerical characters from string
        sanitized_phone = sanitize_phone(phone)

        # verify phone matches format regex
        verify_phone_format(sanitized_phone)

        # assemble our request payload
        payload = dict(
            output=self.output,
            token=self.token,
            phone=sanitized_phone
        )

        # initiate our request
        req = requests.get(self.url, params=payload)

        # if request isn't ok raise for status
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        # attempt to decode json from response, if we can't, raise error
        try:
            data = req.json()
        except ValueError:
            raise InvalidJSONResponseError

        return data

    def lookup_phones_from_workbooks(self):
        """Validates Workbooks against RealValidation DNC API

        Returns
        -------
        list
            List of dicts that contain keys ``row`` and ```response``,
            corresponding to the row of the phone number validated against the
            DNC API and the response back from the DNC API

        """

        rows_and_responses = []

        # for every one of our sheets in `self.workbooks`
        for workbook in self.workbooks:
            for sheet in workbook.sheets:

                # for each row in sheet, lookup phone
                phone_column_index = sheet.phone_column_index
                for row in sheet.get_row_values():

                    if row and row is not None:
                        # get phone from row at phone_column_index
                        phone = row[phone_column_index]

                        # lookup phone
                        try:
                            response = self.lookup_phone(phone)
                        except InvalidPhoneFormatError:
                            response = None

                        # assemble row and response into dict
                        row_and_response = dict(
                            response=response,
                            row=row
                        )

                        # append row and responses
                        rows_and_responses.append(row_and_response)

        return rows_and_responses
