# -*- coding: utf-8 -*-
from lxml import etree
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import lxml
import requests


class EmbeddedPageView(BrowserView):

    template = ViewPageTemplateFile('embeddedpage.pt')

    def __call__(self):
        resource = self.request.form.get('embeddedpage_get_resource', '')
        if resource:
            return requests.get(resource).content
        request_type = self.request['REQUEST_METHOD']
        method = getattr(requests, request_type.lower(), requests.get)
        params = {'url': self.context.url}
        if request_type == 'GET':
            params['params'] = self.request.form
        else:
            params['data'] = self.request.form
        response = method(**params)
        # Normalize charset to unicode
        content = safe_unicode(response.content)
        # Turn to utf-8
        content = content.encode('utf-8')
        el = lxml.html.fromstring(content)
        template = '{0}?embeddedpage_get_resource={1}'
        for script in el.findall('.//script'):
            src = script.attrib.get('src', '')
            if src == '':
                continue
            script.attrib['src'] = template.format(
                self.context.absolute_url(), src)
        if el.find('body'):
            el = el.find('body')
        self.embeddedpage = etree.tostring(el, method='html')
        return self.template()
