import argparse
import os
import re

from configobj import ConfigObj
from builtins import input


class JooTranslate(object):
    paths = {}

    def __init__(self, args):
        """

        :param args: console arguments
        :type args: argparse
        """
        self.args = args
        self.search_pattern = r'(label=|description=|hint=|JText::_\(|JText::script\()(\'|"){1}(.*?)(\'|"){1}'
        self.set_file_paths()

    def read_dir(self):
        """
        reads all php and xml files and searches for regex pattern

        :return void:
        """
        for key, value in self.paths.items():
            patterns = []
            for folder, dirs, files in os.walk(value, topdown=False):
                for filename in files:
                    if filename.endswith(('.php', '.xml')):
                        with open(os.path.join(folder, filename), 'rb') as dest:
                            for l in dest.readlines():
                                try:
                                    pattern = re.search(self.search_pattern, l.decode(('utf8'))).group(3)
                                    if self.args.com.upper() in pattern:
                                        patterns.append(pattern)
                                except:
                                    continue

            self.write_file(value, patterns)

    def write_file(self, path, patterns):
        """
        writes all found patterns to the ini file if pattern not exist

        :param path: the path to administrator or component root
        :type path: str
        :param patterns: list of found translation strings
        :type patterns: list
        :return void:
        """
        lang_file = os.path.join(path, 'language', self.args.lang, self.get_filename())
        if self.args.trans and patterns:
            print('working on %s' % lang_file)

        self._create_dir(lang_file)
        self._create_file(lang_file)

        conf_obj = ConfigObj(lang_file, stringify=True, unrepr=True, encoding='utf-8')
        for p in patterns:
            if not p in conf_obj:
                if self.args.trans:
                    key = input('translation for: %s\n' % p)
                    conf_obj[p] = u'%s' % key
                else:
                    conf_obj[p] = ""
        conf_obj.write()

    def _create_file(self, lang_file):
        """
        create necessary file if not exist

        :param lang_file: path to the language file
        :type lang_file: str
        :return: void
        """
        if not os.path.isfile(lang_file):
            f = open(lang_file, 'w+')
            f.close()

    def _create_dir(self, lang_file):
        """
        create necessary dirs if not exist

        :param lang_file:  path to the language file
        :type lang_file: str
        :return: void
        """
        if not os.path.exists(os.path.dirname(lang_file)):
            os.mkdir(os.path.dirname(lang_file))

    def get_filename(self):
        """

        :return: name of the language ini file
        :rtype: str
        """
        return '%s.%s.ini' % (self.args.lang, self.args.com.lower())

    def set_file_paths(self):
        """
        sets the needed paths to administrator and component part

        :return: void
        """
        self.paths['component'] = os.path.join(self.args.path, 'components', self.args.com)
        self.paths['admin'] = os.path.join(self.args.path, 'administrator', 'components', self.args.com)


def main():
    parser = argparse.ArgumentParser(description='A translation ini file generator for joomla developers')
    parser.add_argument('-s', '--source', dest='path', help="directory to search in", required=True)
    parser.add_argument('-c', '--com', dest='com', help="the name of the component", required=True)
    parser.add_argument('-l', '--lang', dest='lang', default='en-GB', help="language localisation. default is en-GB")
    parser.add_argument('-t', '--translate', dest='trans', action='store_true', help="If you want to translate the strings on console")
    args = parser.parse_args()
    jt = JooTranslate(args=args)
    jt.read_dir()


if __name__ == "__main__":
    main()
