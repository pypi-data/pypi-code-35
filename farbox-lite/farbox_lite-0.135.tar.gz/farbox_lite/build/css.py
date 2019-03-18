#coding: utf8
from scss import Scss
from scss.errors import SassSyntaxError
compiler = Scss()
import os, re

def compile_css(content, filename=None):
    raw_content = content
    if filename and isinstance(filename, (str, unicode)):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in ['.less']:
            content = re.sub(r'@(\w)', '$\g<1>', content)
            content = re.sub(r'\$media ', '@media ', content)
    # remove import tag
    content = re.sub(r'@import.*?[\r\n]', '', content, re.I)
    try:
        to_return = compiler.compile(content)
    except SassSyntaxError, e:
        try:
            message = str(e)
            to_return = '/*%s*/\n%s' % (message, raw_content)
        except:
            to_return = raw_content
    except Exception, e:
        to_return = raw_content

    return to_return




def compile_css_file(filepath):
    if not filepath:
        return
    if not os.path.isfile(filepath):
        return
    with open(filepath, 'rb') as f:
        raw_content = f.read()
    css_content = compile_css(raw_content, filename=os.path.split(filepath)[-1])
    if isinstance(css_content, unicode):
        css_content = css_content.encode('utf8')
    prefix, ext = os.path.splitext(filepath)
    css_filepath = prefix + '.css'
    with open(css_filepath, 'wb') as f:
        f.write(css_content)