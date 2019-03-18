class WirecardFailedInit(Exception):
    pass


class WirecardInvalidCard(Exception):
    pass


class WirecardInvalidRequestedAmount(Exception):
    pass


class WirecardFailedTransaction(Exception):
    def __init__(self, transaction_id, action, statuses):
        self.transaction_id = transaction_id
        self.action = action
        self.statuses = statuses

        super().__init__(transaction_id, action, statuses)
