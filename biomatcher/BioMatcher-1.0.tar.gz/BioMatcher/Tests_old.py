import unittest

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

if __name__ == '__main__':
    # verbosity=2 for more details in console
    unittest.main(verbosity=2)
