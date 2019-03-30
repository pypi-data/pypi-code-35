
import unittest
from inlp.tokenize import *




#@unittest.skip("showing class skipping")
class TokenRemoverTestCase(unittest.TestCase):


    #@unittest.skip("demonstrating skipping")
    def test_remove_single_chars(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        tokens = ['Ñ','®','Ó',"À","Á","Ä","É","Ë","Í","Ò","Ó","Ú","Ü","前","개"]
        t = TokenRemover(lang='english')
        tokens = t.remove_single_chars(tokens)
        print(f"\n\n tokens : {tokens}")
        self.assertEqual(len(tokens), 0)

    #@unittest.skip("demonstrating skipping")
    def test_remove_single_chars__left_exceptions(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        tokens = ['Ñ','®','Ó','R']
        t = TokenRemover(lang='english')
        tokens = t.remove_single_chars(tokens)
        print(f"\n\n tokens : {tokens}")
        self.assertEqual(len(tokens), 1)

    #@unittest.skip("demonstrating skipping")
    def test_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        tokens = ['R','__','--_#_---2.','Ñ','®','Ó',"À","Á","Ä","É","Ë","Í","Ò","Ó","Ú","Ü","前","개"]
        t = TokenRemover(lang='english')
        tokens = t.process(tokens)
        print(f"\n\n tokens : {tokens}")
        self.assertEqual(len(tokens), 1)

    #@unittest.skip("demonstrating skipping")
    def test_remove_single_chars_in_df(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        df = pd.DataFrame({'word':['이런','젠장','쉣']})
        t = TokenRemover(lang='english')
        df = t.remove_single_chars_in_df(df)
        print(f"\n\n df :\n\n{df}")
        self.assertEqual(len(df), 2)






def main():
    unittest.main()
