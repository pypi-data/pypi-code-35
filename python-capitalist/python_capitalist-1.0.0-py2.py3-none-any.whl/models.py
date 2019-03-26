class Model:
    __slots__ = []

    @classmethod
    def parse_json(cls, json_data, **kwargs):
        raise NotImplementedError


class CurrencyRate(Model):
    __slots__ = ['type', 'amount', 'amount_currency', 'target_currency']

    TYPES = ('buy', 'sell', 'uahSell')

    def __init__(self, type_, amount, amount_currency, target_currency):
        self.type = type_
        self.amount = amount
        self.amount_currency = amount_currency
        self.target_currency = target_currency

    @classmethod
    def parse_json(cls, json_data, type_=None, **kwargs):
        return cls(
            type_,
            json_data['amount'],
            json_data['amountCur'],
            json_data['target'],
        )


class Account(Model):
    __slots__ = ['balance', 'blocked_amount', 'currency', 'name', 'number']

    def __init__(self, name, balance, blocked_amount, currency, number):
        self.name = name
        self.balance = balance
        self.blocked_amount = blocked_amount
        self.currency = currency
        self.number = number

    @classmethod
    def parse_json(cls, json_data, **kwargs):
        return cls(
            json_data['name'],
            json_data['balance'],
            json_data['blockedAmount'],
            json_data['currency'],
            json_data['number'],
        )


class BasePayment:
    __slots__ = []

    def get_codename(self):
        raise NotImplementedError

    def get_payment_args(self):
        raise NotImplementedError

    def as_batch_record(self):
        args = [str(self.get_codename())] + [str(a) for a in self.get_payment_args()]
        return ';'.join(args)


class InternalPayment(BasePayment):
    __slots__ = ['capitalist_id', 'amount', 'currency', 'internal_id', 'destination']

    def __init__(self, capitalist_id, amount, currency, internal_id, destination):
        self.capitalist_id = capitalist_id
        self.amount = amount
        self.currency = currency
        self.internal_id = internal_id
        self.destination = destination

    def get_codename(self):
        return 'CAPITALIST'

    def get_payment_args(self):
        return self.capitalist_id, self.amount, self.currency, self.internal_id, self.destination


class WebMoneyPayment(BasePayment):
    __slots__ = ['wm_id', 'amount', 'currency', 'internal_id', 'destination', 'protection_code', 'protection_period']

    def __init__(
            self, wm_id, amount, currency, internal_id, destination, protection_code=None, protection_period=None):
        self.wm_id = wm_id
        self.amount = amount
        self.currency = currency
        self.internal_id = internal_id
        self.destination = destination
        self.protection_code = protection_code
        self.protection_period = protection_period

    def get_codename(self):
        return 'WM'

    def get_payment_args(self):
        args = [self.wm_id, self.amount, self.currency, self.internal_id, self.destination, self.protection_code,
                self.protection_period]
        return [arg for arg in args if arg is not None]


class CardRussianPayment(BasePayment):
    __slots__ = ['card_number', 'amount', 'currency', 'internal_id', 'destination']

    def __init__(self, card_number, amount, currency, internal_id, destination):
        self.card_number = card_number
        self.amount = amount
        self.currency = currency
        self.internal_id = internal_id
        self.destination = destination

    def get_codename(self):
        return 'RUCARD'

    def get_payment_args(self):
        args = [self.card_number, self.amount, self.currency, self.internal_id, self.destination]
        return [arg for arg in args if arg is not None]


class CardWorldwidePayment(BasePayment):
    __slots__ = [
        'card_number', 'amount', 'currency', 'internal_id', 'destination', 'card_first_name', 'card_last_name',
        'birthday_date', 'address', 'country_alpha2', 'city', 'card_expiration_month', 'card_expiration_year']

    def __init__(
            self, card_number, amount, currency, internal_id, destination, card_first_name, card_last_name,
            birthday_date, address, country_alpha2, city, card_expiration_month, card_expiration_year):
        self.card_number = card_number
        self.amount = amount
        self.currency = currency
        self.internal_id = internal_id
        self.destination = destination
        self.card_first_name = card_first_name
        self.card_last_name = card_last_name
        self.birthday_date = birthday_date
        self.address = address
        self.country_alpha2 = country_alpha2
        self.city = city
        self.card_expiration_month = card_expiration_month
        self.card_expiration_year = card_expiration_year

    def get_codename(self):
        return 'WORLDCARD'

    def get_payment_args(self):
        return (
            self.card_number, self.amount, self.currency, self.internal_id, self.destination, self.card_first_name,
            self.card_last_name, self.birthday_date, self.address, self.country_alpha2, self.city,
            self.card_expiration_month, self.card_expiration_year)
