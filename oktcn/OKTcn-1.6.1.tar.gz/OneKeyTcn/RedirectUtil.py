import requests, re, time
import OneKeyTcn.IdentifyURLUtil as IdentifyURLUtil
import NorrisUtils.BuildConfig

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
}


# 迭代溯源
# 支持插入log方法已经插入中断逻辑的溯源
def iterateRedirect(url, pausefunc=None, logfunc=None):
    try:
        # 由中断方法判定
        if pausefunc != None and pausefunc(url):
            return url
        req = requests.get(url, headers=headers, allow_redirects=False)
        status_code = req.status_code
        if logfunc != None:
            logfunc(status_code)
        # 302 表示重定向，在返回的headers里Location处标识
        if status_code == 302 or status_code == 301:
            headers_location_ = req.headers['Location']
            if(headers_location_.startswith('//')):
                if logfunc != None:
                    logfunc(req.headers)
                    logfunc('溯源成功！原始地址为：【' + url + '】')
                return url
            if logfunc != None:
                logfunc(req.headers)
                logfunc('检测到重定向，正在帮您溯源...')
            return iterateRedirect(headers_location_, pausefunc, logfunc)
        else:
            if(IdentifyURLUtil.isJDShortUnion(url)):
                jdc_url = IdentifyURLUtil.extractJDCUrl(req.text)
                if(jdc_url!=None):
                    return iterateRedirect(jdc_url, pausefunc, logfunc)
            if logfunc != None:
                logfunc(req.headers)
                logfunc('溯源成功！原始地址为：【' + url + '】')
            return url
    except Exception as e:
        print(e)
        return url


# 批量溯源，找到原文中url的原地址
def batchRedirect(text, logfunc=None, delay=0):
    results = text
    # pattern = re.compile('http(s)://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?')
    pattern = re.compile('[a-zA-z]+://[^\s]*')
    items = re.findall(pattern, text)
    for item in items:
        redirect = iterateRedirect(item, logfunc=logfunc)
        if logfunc != None:
            logfunc(item)
            logfunc(redirect)
        results = results.replace(item, redirect)
        time.sleep(delay)

    if logfunc != None:
        logfunc(results)
    return results



if NorrisUtils.BuildConfig.DebugBackDoor:
    str = '''A、常规签到-京豆
    领京豆 
    http://t.cn/RdNtSt1
    京东会员 
    http://t.cn/RpFEyqd
    京豆乐园 http://t.cn/RuLvpAU
    每日福利 http://t.cn/RH151So
    拍拍签到 http://t.cn/R33hjAY
    京豆寻宝 http://t.cn/RdNtStm'''
    # print(iterateRedirect('http://t.cn/RdNtSt1'))
    # print(IdentifyURLUtil.isJDUrl('https://bean.m.jd.com/rank/index.action'))
    print(batchRedirect(str, logfunc=print, delay=1))
