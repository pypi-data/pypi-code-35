from .evaluators import get_evaluator


class Communicator(object):
    def __init__(self):
        pass

    def login(self, user):
        return True
        #password = getpass('Enter password:')
        #if user == '71296' and password == 'password':
        #    return True
        #return False


class OLJ(object):
    def __init__(self, user):
        self.matricola = user
        self.com = Communicator()

        if not self.com.login(user):
            raise Exception("Unauthorized.")

    def evaluate(self, fn):
        evaluator = get_evaluator(fn)
        evaluator(fn)



