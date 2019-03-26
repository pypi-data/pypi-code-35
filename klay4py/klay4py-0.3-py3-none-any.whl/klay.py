import os

from pyKlay import jvm

__all__ = ['Klay']

class Klay:

    def __init__(self, config_file_path='./data/configuration/klay.conf'):

        jvm.init_jvm()
        self._klay_ep = jvm.get_jvm().klay.python.wrapper.KlayEntryPoint(config_file_path)


    def do_klay(self, sentence):
        return self._klay_ep.doKlay(sentence)


if __name__ == '__main__':
    klay = Klay()

    text = '① 대한민국은 민주공화국이다. ② 대한민국의 주권은 국민에게 있고, 모든 권력은 국민으로부터 나온다.'

    morphs = klay.do_klay(text)
    for morph in morphs.iterator():
        print(morph)