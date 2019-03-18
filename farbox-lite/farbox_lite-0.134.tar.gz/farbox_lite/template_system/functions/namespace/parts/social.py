#coding: utf8
from __future__ import absolute_import

from farbox_lite.utils import smart_unicode
from farbox_lite.utils.lazy import get_value_from_data
from flask import g

social_prefixes = {
    'twitter': 'https://twitter.com',
    'instagram': 'http://instagram.com',
    'dribbble': 'https://dribbble.com',
    'github': 'https://github.com',
    'quora': 'https://quora.com',
    'flickr': 'https://www.flickr.com/photos',
    'weibo': 'http://www.weibo.com',
    'facebook': 'https://www.facebook.com',
    'pinterest': 'http://pinterest.com',
    'vimeo': 'https://vimeo.com',
    'telegram': 'https://telegram.me',
    'youtube': 'https://www.youtube.com',
    'zhihu': 'https://www.zhihu.com/people',
    '500px': 'https://500px.com',
}


social_icons= {
    'twitter': 'fa fa-twitter',
    'instagram': 'fa fa-instagram',
    'dribbble': 'fa fa-dribbble',
    'github': 'fa fa-github',
    'quora': 'fa fa-question-circle-o',
    'flickr': 'fa fa-flickr',
    'weibo': 'fa fa-weibo',
    'facebook': 'fa fa-facebook',
    'pinterest': 'fa fa-pinterest',
    'vimeo': 'fa fa-vimeo',
    'telegram': 'fa fa-send-o',
    'youtube': 'fa fa-youtube',
    '500px': 'fa fa-500px',
}


social_names = social_prefixes.keys()



def get_social_items():
    items = []
    site_configs = get_value_from_data(g, 'site.configs') or {}
    for social_name in social_names:
        username = smart_unicode((site_configs.get(social_name) or '')).strip()
        if not username:
            continue
        social_url_prefix = social_prefixes.get(social_name.lower())
        if '://' in username:
            url = username # 本身就是一个完整的链接
        elif social_url_prefix:
            url = social_url_prefix + '/' + username.split('/')[-1]
        else:
            url = '#'
        item = dict(
            service = social_name,
            username = username,
            url = url,
            icon_class = social_icons.get(social_name) or 'fa fa-link',
        )
        items.append(item)
    return items


def get_social_links():
    social_items = get_social_items()
    if not social_items:
        return ''

    html = ''
    for social_item in social_items:
        html += '<a href="%s" title="%s"><i class="%s"></i></a>\n' % (social_item['url'], social_item['service'], social_item['icon_class'])
    html = '<div class="my_socials">\n%s\n</div>' % html
    return html
