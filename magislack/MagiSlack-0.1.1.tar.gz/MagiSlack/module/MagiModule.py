import time
import threading


class MagiModule:
    __cooltime = 0
    __user_list = {}
    __timer_thread = threading.Thread()
    slack_token = ''

    def __init__(self, slack_token, cooltime=3):
        self.__cooltime = cooltime
        self.__timer_thread = threading.Thread(target=self.__user_timer)
        self.__timer_thread.daemon = True
        self.__timer_thread.start()
        self.slack_token =slack_token

    def __del__(self):
        self.__timer_thread.is_run = False

    def __user_timer(self):
        t = threading.current_thread()
        while getattr(t, 'is_run', True):
            for user in self.__user_list:
                self.__user_list[user] = lambda x: x+1 if x < self.__cooltime else self.__cooltime

            time.sleep(1)

    def user_own_exp(self, username, exp):
        assert isinstance(username, str)
        assert isinstance(exp, int)

        # TODO:
        #   DB exp earn code

    def is_user_can_get_exp(self, username):
        assert isinstance(username, str)

        if self.__user_list[username] >= self.__cooltime:
            return True
        else:
            return False
