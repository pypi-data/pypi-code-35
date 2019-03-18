from .argparser import parser
from .realvalidation import RealValidation
from .utils import write_rows_to_workbook, is_dnc_json_response_on_dnc
from . import logger

from .errors import ResponseCodeNotOkError

import logging
import tempfile

log = logging.getLogger(__name__)


def main():
    args = parser.parse_args()

    realvalidation = RealValidation(
        token=args.api_token,
        url=args.api_url,
        staging=args.staging
    )

    for workbook in args.workbook:
        realvalidation.add_workbook(workbook)

    rows_and_responses = realvalidation.lookup_phones_from_workbooks()

    temp_dir = tempfile.mkdtemp(prefix='realvalidation')

    # TODO: implement util function
    dnc_rows = []
    valid_rows = []
    error_rows = []

    for row_and_response in rows_and_responses:
        row = row_and_response.get('row')
        response = row_and_response.get('response')

        if response is not None:
            try:
                if is_dnc_json_response_on_dnc(response):
                    dnc_rows.append(row)
                else:
                    valid_rows.append(row)
            # TODO: maybe we could add error data to row array, that way when
            # we view the error sheet, we can determine which error triggered
            except ResponseCodeNotOkError:
                error_rows.append(row)
        else:
            error_rows.append(row)

    write_rows_to_workbook(dnc_rows, temp_dir, 'dnc')
    write_rows_to_workbook(valid_rows, temp_dir, 'valid')
    write_rows_to_workbook(error_rows, temp_dir, 'error')

    log.debug('written to "{}"'.format(temp_dir))


if __name__ == '__main__':
    main()
