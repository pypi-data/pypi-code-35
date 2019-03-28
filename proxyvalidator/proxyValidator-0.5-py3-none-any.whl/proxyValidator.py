from random import choice
from requests import Session
from threading import Thread

class ProxyValidator:
    def __init__(self):
        self.validated_proxies = []
        self.job_threads = []

    def __run_function(self, function, function_argument):
        job_thread = Thread(target=function, args=(function_argument,))
        job_thread.setDaemon(True)
        self.job_threads.append(job_thread)
        job_thread.start()

    
    def validate_proxies(self, proxies):
        for proxy in proxies:
            self.__run_function(self.__validate_proxy, proxy)
        for job_thread in self.job_threads:
            job_thread.join()
    
    def __validate_proxy(self, proxy):
        session = Session()
        session.proxies = {'https': f'https://{proxy}'}
        try:
            session.get('http://www.showmemyip.com/')
            self.validated_proxies.append(proxy)
            print(f'proxy: {proxy} validated')
        except:
            print(f'proxy: {proxy} unvalidated')
            pass