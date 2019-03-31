import unittest

from .. import PluginManager
from .. import SignalManager

from .mocks import sine_wave


class TestSignalManager(unittest.TestCase):
    @staticmethod
    def smoke_test():
        print('smoke_test')
        SignalManager()

    def register_plugin_test(self):
        print('custom_plugin_test')

        class TestPlugin(PluginManager):
            def __init__(self):
                super().__init__()
                self.custom = []

            def custom_function(self):
                return self.custom

        SignalManager.register_plugin(TestPlugin)

        self.assertTrue(TestPlugin in SignalManager.__bases__,
                        'TestPlugin should be a subclass of the PluginManager')

        sig = SignalManager()
        self.assertEqual([], sig.custom_function())

    def add_history_test(self):
        print('add_history_test')

        sig = SignalManager(generator=sine_wave())

        sig.remove_channel('sine', )

        self.assertEqual(["remove_channel('sine', )"], sig.history)

    def add_history_test(self):
        print('add_history_test')

        sig = SignalManager(generator=sine_wave())

        sig.remove_channel('sine', )

        self.assertEqual(["remove_channel('sine', )"], sig.history)

    def extract_channel_test(self):
        print('add_history_test')

        data = {
            'fs': 512,
            'num_channels': 3,
            'channel_names': ['sine1', 'sine2', 'sine3'],
            'epochs': 1
        }

        sig = SignalManager(generator=sine_wave(data=data))

        sig.extract_channels(['sine2', 'sine3'])

        self.assertEqual(sig.num_channels, 2)
        self.assertEqual(sig.channel_names, ['sine2', 'sine3'])
        self.assertEqual(sig.data.shape, (1, 2, 10240))


if __name__ == '__main__':
    unittest.main()
