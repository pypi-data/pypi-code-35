import base64
import calendar
import multiprocessing
import re
from datetime import datetime, date, timedelta

from pytz import timezone
from schematics.exceptions import ValidationError


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


# def pub_sub_message(schemma: BaseSchema, operation: str) -> PubSubMessage:
#     message = PubSubMessage()
#     message.message = schemma
#     message.operation = operation
#     return message


def get_cache_time() -> int:
    """
    Define cache time based in how many seconds are remaining between now and midnight
    :return: Integer
    """
    today = datetime.today().date().isoformat()
    brazil_timezone = timezone('America/Sao_Paulo')
    end_day = datetime.strptime(f'{today}T23:59:59.999999-0300', '%Y-%m-%dT%H:%M:%S.%f%z')
    now = datetime.now(tz=brazil_timezone)
    cache_seconds = (end_day - now).seconds
    return cache_seconds


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def base64_encode(value: str) -> bytes:
    return base64.b64encode(bytes(value, 'utf-8'))


def base64_decode(value: str) -> bytes:
    return base64.b64decode(bytes(value, 'utf-8'))


def sanitize_html_data(html_text: 'Tag') -> str:
    return html_text.text.replace('\n', '').replace('  ', '').strip()


def get_digit_only(text: str) -> str:
    return ''.join([x for x in text if x.isdigit()])


def get_only_upper(text: str) -> str:
    return ''.join([x for x in text if x.isupper()])


def check_weekday(date: datetime) -> bool:
    return date.weekday() in [5, 6]


def get_weekday(date: datetime) -> datetime:
    while check_weekday(date):
        date = date + timedelta(days=1)
    return date


def is_not_null(value):
    if value is not None:
        return value
    raise ValidationError('Value must be informed')


def is_cpf_valid(cpf):
    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """

    non_digit = re.compile(r'[^0-9]')

    cpf = non_digit.sub('', cpf)

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números:
    if len(numbers) != 11:
        raise ValidationError('CPF is invalid.')

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValidationError('CPF is invalid.')

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValidationError('CPF is invalid.')

    return cpf


def is_cnpj_valid(cnpj):

    """Check whether CNPJ is valid. Optionally pad if too short."""
    cnpj_first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj_second_weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    non_digit = re.compile(r'[^0-9]')

    cnpj = non_digit.sub('', cnpj)

    # all complete CNPJ are 14 digits long
    if len(cnpj) != 14:
        raise ValidationError('CNPJ is invalid.')

    # 0 is invalid; smallest valid CNPJ is 191
    if cnpj == '00000000000000':
        raise ValidationError('CNPJ is invalid.')

    digits = [int(k) for k in cnpj[:13]]  # identifier digits
    # validate the first check digit
    cs = sum(w * k for w, k in zip(cnpj_first_weights, digits[:-1])) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[12]):
        raise ValidationError('CNPJ is invalid.')  # first check digit is not correct
    # validate the second check digit
    cs = sum(w * k for w, k in zip(cnpj_second_weights, digits)) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[13]):
        raise ValidationError('CNPJ is invalid.')  # second check digit is not correct
    # both check digits are correct
    return cnpj
