import extractorblog

et = extractorblog.get('https://www.jiqizhixin.com/articles/2019-03-20-14')
print(et.getHtml)
print(et.getMarkdown)