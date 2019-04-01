##!/usr/bin/env python
#encoding:utf-8

import re
import sys
from urllib import request
from colored import fg, attr

colors = {
    'word': fg('red'),
    'soundmark': fg('green'),
    'definition': fg('yellow'),
    'example-eng': fg('cyan'),
    'example-chn': fg('magenta')
}

url = 'https://dict.youdao.com/w/eng/'


def search(word):
    global url
    site = url + word
    req = request.Request(site)
    response = request.urlopen(req)

    return response.read().decode('utf-8')


def getSoundmark(html):
    pa = re.compile('<span class="phonetic">(.*?)</span>')
    soundmark = pa.findall(html)

    return soundmark


def getDefinition(html):
    pa_container = re.compile(
        '<div class="trans-container">.*?<ul>(.*?)</ul>.*?</div>', re.S)
    ma_container = pa_container.search(html)
    definition = []

    if ma_container:
        str_container = ma_container.group(1)
        pdef = re.compile('<li>(.*?)</li>')
        items = pdef.findall(str_container)
        for item in items:
            definition.append(item)

    return definition


def getExamples(html):
    examples = []
    pa_bilingual = re.compile('<div id="bilingual".*?>(.*?)</div>', re.S)
    pa_group = pa_bilingual.search(html)
    if pa_group:
        ma_bilingual = pa_group.group()
    else:
        return []
    pa_p = re.compile('<p>(.*?)</p>', re.S)
    ma_p = pa_p.findall(ma_bilingual)
    pa_span = re.compile('<span.*?>(.*?)</span>', re.S)
    for item in ma_p:
        ma_span = pa_span.findall(item)
        exi = ''
        for w in ma_span:
            exi += w
        exi = re.sub('<.?\w>', '', exi)
        examples.append(exi)

    return examples


def outputformat(word, soundmarks, definitions, examples, color=colors):
    outstr = ''

    #word format
    outstr += '%s {0} %s\n'.format(word) % (color['word'], attr(0))
    #soundmarks
    for soundmark in soundmarks:
        outstr += '%s {0} %s'.format(soundmark) % (color['soundmark'], attr(0))
    outstr += '\n'
    #definitions
    for definition in definitions:
        outstr += '%s {0} %s\n'.format(definition) % (color['definition'],
                                                      attr(0))
    #examples
    for i in range(len(examples)):
        example = examples[i]
        if i % 2 == 0:
            outstr += '%s {0} %s\n'.format(example) % (color['example-eng'],
                                                       attr(0))
        else:
            outstr += '%s {0} %s\n'.format(example) % (color['example-chn'],
                                                       attr(0))

    print(outstr)


def main():
    word = sys.argv[1] 
    html = search(word)
    soundmarks = getSoundmark(html)
    definitions = getDefinition(html)
    examples = getExamples(html)
    outputformat(word, soundmarks, definitions, examples)


if __name__ == '__main__':
    main()
