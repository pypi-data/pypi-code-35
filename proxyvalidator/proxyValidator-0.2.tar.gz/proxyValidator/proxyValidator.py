from random import choice
from requests import Session
from threading import Thread

class ProxyValidator:
    def __init__(self, proxies_to_validate):
        self.validated_proxies = []
        self.__validate_proxies(proxies_to_validate)

    @staticmethod
    def __run_function(function, function_argument):
        job_thread = Thread(target=function, args=(function_argument,))
        job_thread.start()
    
    def __validate_proxies(self, proxies):
        for proxy in proxies:
            self.__run_function(self.__validate_proxy, proxy)
    
    def __validate_proxy(self, proxy):
        session = Session()
        session.proxies = {'https': f'https://{proxy}'}
        try:
            session.get('http://www.showmemyip.com/')
            self.validated_proxies.append(proxy)
        except:
            pass