# -*- coding: utf-8 -*-
import re,os
from bs4 import BeautifulSoup
import requests
from w3lib.html import remove_tags
class BodyExtractor():
    def __init__(self, html, encoding='utf-8'):
        if type(html) == bytes:
            self.html = html.decode(encoding)
        else:
            self.html = html
        self.pureText = ''  # 去除标签后的
        self.THRESHOLD = 50  # 骤升点阈值
        self.K = 3  # 行块中行数
        self.wordCount = []  # 每个行块中的字符个数
        self.lines = []
        self.content = ''  # 抽取的正文
        self.title = ''
        self.author=''
        self.form=''
        self.time=''
        self.img=''
        self.file=''
        self.maxIndex = -1  # 字符最多的行块索引
        self.start = -1
        self.end = -1
        self._preprocess()
        self._start()
        self._end()

        if self.end != -1:
            # print(self.lines)
            self.content = ''.join(self.lines[self.start:self.end + self.K - 1])

    def _preprocess(self):
        regex = re.compile(
            r'(?:<!DOCTYPE.*?>)|'  # doctype
            r'(?:<head[\S\s]*?>[\S\s]*?</head>)|'
            r'(?:<!--[\S\s]*?-->)|'  # comment
            r'(?:<img[\s\S]*?>)|'  # 图片
            r'(?:<br[\s\S]*?>\s*[\n])|'
            r'(?:<script[\S\s]*?>[\S\s]*?</script>)|'  # js...
            r'(?:<style[\S\s]*?>[\S\s]*?</style>)', re.IGNORECASE)  # css
        regTitle = re.search('<title>[\s\S]*?</title>',self.html)
        reg=re.findall(r'作者：\s+(.*?)\s+<',self.html)
        req1=re.findall(r'来源：\s+(.*?)\s+<',self.html)
        reqTime=re.search(r'(\d{4}-\d{1,2}-\d{1,2})',self.html)
        reqImg=re.findall( r'<img[\s\S]*?>',self.html)
        reqFile=re.findall(r'<a.*?href="(.*?)".*>',self.html)
        if regTitle is not None:
            titleTag = regTitle.group()
            self.title = titleTag[7:len(titleTag)-8]
        if reg is not None:
            try:            
                self.author=remove_tags(reg[0])
            except:
                print('本文无作者')
        if req1 is not None:
            try:            
                self.form=remove_tags(req1[0])
            except:
                req11=re.findall(r'>来源：(.*?)<',self.html)
                self.form=req11[0]
        if reqTime is not None:
            reqTag = reqTime.group(0)
            self.time=reqTag
        if reqImg is not None:
            f=[]
            for x in reqImg:
                b=re.findall(r'<img\s+src="(.*?)".*?',x)
                try:
                    imgs=os.path.splitext(b[0])
                    filename,type=imgs
                    if 'public' not in b[0] and type !='.gif':                    
                        f.append(b[0])
                except:
                    pass
            self.img=f
        if reqFile is not None:
            k=[]
            for ss in reqFile:
                files=os.path.splitext(ss)
                filename,type=files
                if type == '.pdf' or type =='.doc' or type =='.xlsx' or type =='zip':
                    k.append(ss)
            if k:
                self.file=set(k)
                    
        filteredHtml = self.html_escape(regex.sub('', self.html))
        self.pureText = BeautifulSoup(filteredHtml, 'lxml').get_text()
        self.lines = list(map(lambda s: re.sub(r'\s+', '', s), self.pureText.splitlines()))
        count = list(map(lambda s: len(s), self.lines))
        for i in range(len(count) - self.K + 1):
            self.wordCount.append(count[i] + count[i + 1] + count[i + 2])
        self.maxIndex = self.wordCount.index(max(self.wordCount))

    def html_escape(self,text):
        """
        html转义
        """
        text = (text.replace("&quot;", "\"").replace("&ldquo;", "“").replace("&rdquo;", "”")
                .replace("&middot;", "·").replace("&#8217;", "’").replace("&#8220;", "“")
                .replace("&#8221;", "\”").replace("&#8212;", "——").replace("&hellip;", "…")
                .replace("&#8226;", "·").replace("&#40;", "(").replace("&#41;", ")")
                .replace("&#183;", "·").replace("&amp;", "&").replace("&bull;", "·")
                .replace("&lt;", "<").replace("&#60;", "<").replace("&gt;", ">")
                .replace("&#62;", ">").replace("&nbsp;", " ").replace("&#160;", " ")
                .replace("&tilde;", "~").replace("&mdash;", "—").replace("&copy;", "@")
                .replace("&#169;", "@").replace("♂", "").replace("\r\n|\r", "\n"))
        return text

    def _start(self):
        for i in [-x - 1 + self.maxIndex for x in range(self.maxIndex)]:
            gap = min(self.maxIndex - i, self.K)
            if sum(self.wordCount[i + 1:i + 1 + gap]) > 0:
                if self.wordCount[i] > self.THRESHOLD:
                    continue
                else:
                    break

        self.start = i + 1

    def _end(self):
        for i in [x + self.maxIndex for x in range(len(self.wordCount) - self.maxIndex - 2)]:
            if self.wordCount[i] == 0 and self.wordCount[i + 1] == 0:
                self.end = i
                break

if __name__ == '__main__':
    url = ['http://md.tech-ex.com/', 'http://md.tech-ex.com/ired/2016/47848.html',
           'http://md.tech-ex.com/medical/2016/47829.html',
           'http://md.tech-ex.com/medical/2016/47834.html',
           'http://md.tech-ex.com/ired/2016/47899.html',
           'http://md.tech-ex.com/engineering/2016/47831.html',
           'http://view.news.qq.com/original/intouchtoday/n3711.html',
           'http://news.qq.com/a/20161115/034143.htm']
    res = requests.get(url[7])
    if res.encoding != 'ISO-8859-1' or res.encoding != 'utf-8':
        extractor = BodyExtractor(res.content,encoding=res.encoding)
    else:
        extractor = BodyExtractor(res.content)
    print(extractor.content)
    #print(extractor.lines)
    print(extractor.title)