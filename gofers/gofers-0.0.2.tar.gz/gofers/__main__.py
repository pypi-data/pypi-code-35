import sys
from .classmodule import MyClass
from .functionmodule import my_function


def main():
    # 以下内容中的参数解析方式并不好，这里只是为了简单
    # 最好使用argparse或者click模块做这方面的工具
    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))

    for arg in args:
        print('passed argument :: {}'.format(arg))
        my_function('hello world')
        my_object = MyClass('Thomas')
        my_object.say_name()


if __name__ == '__main__':
    main()
