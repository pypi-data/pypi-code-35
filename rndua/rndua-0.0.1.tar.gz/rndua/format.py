class Formatter:

    def __init__(self):
        return

    def os_x_version_to_firefox(self,version):
        ver=version.split('.')
        return 'Macintosh; Intel Mac OS X %s.%s'%(ver[0],ver[1])

    def os_x_version_to_chrome(self,version):
        return ''.join(['Macintosh; Intel Mac OS X ',version.replace('.','_')])

    def windows_nt_version_to_ua(self,version,arch=''):
        return ''.join(['Windows NT ',version,arch])

    def linux_distro_to_ua(self,distro,arch='x86_64'):
        return ''.join(['X11; ',distro,'Linux ',arch])

    def android_environment_to_ua(self,env,lang='',firefox=False):
        res=['Linux; ']
        if lang!='': # old Android Browser
            res.append('U; ')
        res.append('Android ')
        if env[1]=='9.0.0':
            res.append('9')
        elif env[1].startswith('8'):
            res.append(env[1])
        elif env[1].endswith('.0'):
            res.append(env[1][:-2])
        else:
            res.append(env[1])
        res.append('; ')
        if lang!='':
            res.extend([lang,'; '])
        elif firefox:
            res.append('Mobile')
            return ''.join(res)
        res.extend([env[2],' Build/',env[0]])
        return ''.join(res)

    def format_firefox_ua(self,dev_ua,version,desktop=True):
        res=['Mozilla/5.0 (',dev_ua,'; rv:',version,') Gecko/']
        if desktop:
            res.append('20100101')
        else:
            res.append(version)
        res.extend([' Firefox/',version])
        return ''.join(res)

    def format_chrome_ua(self,dev_ua,version):
        res=['Mozilla/5.0 (',dev_ua,') AppleWebKit/',version[1],
                ' (KHTML, like Gecko) Chrome/',version[0],' Safari/',
                version[1]]
        return ''.join(res)

    def format_android_browser_ua(self,dev_ua,webkit_version='534.30'):
        res=['Mozilla/5.0 (',dev_ua,') AppleWebKit/',webkit_version,
                ' (KHTML, like Gecko) Version/4.0 Safari/',webkit_version]
        return ''.join(res)
