from abc import abstractmethod
from typing import Iterable, Iterator


class RuleFacts(Iterable):
    """
    条件事实.key表示了一个规则因子的名字. value表示的是事实的值
    """

    def __init__(self,key:str=None,value=None,facts:dict=None) -> None:
        self.__facts = facts or {}
        if key is not None:
            self.add_fact(key,value)

    def add_fact(self, key:str, value):
        self.__facts[key] = value

    def add_facts(self, rule_facts):
        self.__facts.update(rule_facts.get_facts())

    def get_facts(self)->dict:
        return self.__facts

    def get_fact(self,key:str):
        # 这里需要使用python表达式或至少是点号表达式.  因为别个可能是 a.b.c 这样写的
        pass

    def __iter__(self) -> Iterator:
        return self.__facts.__iter__()

class IRuleListener:

    @abstractmethod
    def before_evaluate(self, rule, facts)->bool:
        """
        在一个规则比较前触发
        :param rule:
        :param facts:
        :return: true表示继续往下走,false表示强制取消这个规则的比较
        """
        pass

    @abstractmethod
    def after_evaluate(self, rule, facts, evaluation_result:bool):
        """
        比较后触发
        :param rule:
        :param facts:
        :param evaluation_result: 表示比较的结果
        :return:
        """
        pass

    @abstractmethod
    def before_action(self, rule, facts)->bool:
        """
        执行action动作前触发
        :param rule:
        :param facts:
        :return: true表示继续往下走,false表示不执行这个规则的action
        """
        pass

    @abstractmethod
    def on_success(self, rule, facts, result):
        """
        在action动作成功后触发
        :param rule:
        :param facts:
        :param result:
        :return:
        """
        pass

    @abstractmethod
    def on_failure(self, rule, facts, exception:Exception):
        """
        在action动作失败后触发
        :param rule:
        :param facts:
        :param exception:
        :return:
        """
        pass