

class SoftAsserts(object):

    def __init__(self):
        self.errors = []

    def should(self, condition):
        return condition.write_to(self.errors)

    def is_true(self, condition, msg: str = None) -> bool:
        res = bool(condition)
        if not res:
            message = msg or f'Not true: \n\t{res}'
            self.errors.append(message)
        return res

    def is_false(self, condition, msg: str = None) -> bool:
        res = bool(condition)
        if res:
            message = msg or f'Not false: \n\t{res}'
            self.errors.append(message)
        return res

    def is_equal(self, current, expected, msg: str = None) -> bool:
        message = msg or f'Not equal: \n\tcurrent={current}\n\texpected={expected}'
        return self.is_true(current == expected, message)

    def is_not_equal(self, current, expected, msg: str = None) -> bool:
        message = msg or f'Equal: \n\tcurrent={current}\n\texpected={expected}'
        return self.is_true(current != expected, message)

    def is_contain(self, item, container, msg: str = None) -> bool:
        message = msg or f'Not contain: \n\titem={item}\n\tcontainer={container}'
        return self.is_true(item in container, message)

    def is_not_contain(self, item, container, msg: str = None) -> bool:
        message = msg or f'Contain: \n\titem={item}\n\tcontainer={container}'
        return self.is_true(item not in container, message)

    def is_not(self, current, expected):
        # check.is_not - a is not b
        pass

    def is_none(self):
        # check.is_none - x is None
        pass

    def is_not_none(self):
        # check.is_not_none - x is not None
        pass

    def is_instance(self):
        # check.is_instance - isinstance(a, b)
        pass

    def is_not_instance(self):
        # check.not_is_instance - # not isinstance(a, b)
        pass

    def is_greater(self):
        # check.greater - a > b
        pass

    def is_greater_equal(self):
        # check.greater_equal - a >= b
        pass

    def is_less(self):
        # check.less - a < b
        pass

    def is_less_equal(self):
        # check.less_equal - a <= b
        pass

    def is_schema(self, current, expected):
        pass
