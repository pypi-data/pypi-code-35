from django.db import transaction
from apimas.base import ProcessorFactory


class BeginTransaction(ProcessorFactory):
    def process(self, runtime_data):
        ctx = transaction.Atomic(using=None, savepoint=True)
        ctx.__enter__()
        return {'guards/transaction_begin': ctx}

    def cleanup(self, name, exc, data):
        runtime = data['$runtime']
        ctx = runtime['guards/transaction_begin']
        ctx.__exit__(type(exc), exc, None)
        return {'guards/transaction_begin': False}


class CommitTransaction(ProcessorFactory):
    def process(self, runtime_data):
        ctx = runtime_data['guards/transaction_begin']
        ctx.__exit__(None, None, None)
        return {'guards/transaction_commit': True}
