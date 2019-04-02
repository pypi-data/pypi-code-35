import sys, os

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TEST_ROOT + '/../')
from jootranslate.cli import JooTranslate

class Args(object):
    path = os.path.join(TEST_ROOT, 'files')
    com = 'com_test'
    lang = 'en-GB'
    trans = False


class TestCli(object):
    @classmethod
    def setup_class(cls):
        args = Args()
        cls.jt = JooTranslate(args=args)
        cls.jt.read_dir()
        cls.admin_lang = os.path.join(cls.jt.paths['admin'], 'language', args.lang, cls.jt.get_filename())
        cls.com_lang = os.path.join(cls.jt.paths['component'], 'language', args.lang, cls.jt.get_filename())

    @classmethod
    def teardown_class(cls):
        rf = open(cls.admin_lang, 'r')
        lines = rf.readlines()
        rf.close()
        wf = open(cls.admin_lang, 'w')
        wf.writelines(lines[:1])
        wf.close()

        os.remove(cls.com_lang)
        os.rmdir(os.path.dirname(cls.com_lang))

    def test_files_exist(self):
        assert os.path.isfile(self.admin_lang)
        assert os.path.isfile(self.com_lang)

    def test_file_content(self):
        af = open(self.admin_lang, 'r')
        assert af.read() == "COM_TEST_KEEPME = 'translated'\nCOM_TEST_TEST_STRING = ''\n"
        af.close()
        cf = open(self.com_lang, 'r')
        assert cf.read() == "COM_TEST_TEST_STRING = ''\nCOM_TEST_JS_STRING = ''\nCOM_TEST_FORM = ''\n"
        cf.close()
