#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2019 Etienne Robillard <tkadm30@yandex.com>
# All rights reserved.
# Please see the "LICENSE" file for license details. 

#import logging
#import datetime

import base64
from urllib.parse import urlparse, urljoin

#from BeautifulSoup import BeautifulSoup
#log = logging.getLogger(__name__)

import PyRSS2Gen

from notmm.dbapi.orm.decorators import with_schevo_database
from notmm.utils.wsgilib import HTTPNotFound, HTTPResponse

def url_for(environ, url):
    if 'HTTPS' in environ:
        proto = 'https'
    else:
        proto = 'http'
    host = environ['HTTP_HOST']
    return urljoin("%s://%s" % (proto, host), url, allow_fragments=False)

@with_schevo_database('127.0.0.1:4545')
def index(request, **kwargs):
    db = request.environ['schevo.db.zodb']
    messages = db.Message.find()
    messages.reverse()
    xml = PyRSS2Gen.RSS2(
        title="BlogEngine2 RSS",
        link=url_for(request.environ, '/blog/'),
        description="Recent posts"
    )
    for msg in messages:
        xml.items.append(PyRSS2Gen.RSSItem(
            title=''.join(
                #BeautifulSoup(msg.content).findAll(text=True)
                msg.content
                ),
            link=url_for(request.environ, msg.get_absolute_url())
            ))
    return HTTPResponse(xml.to_xml(), mimetype='text/xml')

#@authorize(RemoteUser())
@with_schevo_database('127.0.0.1:4545')
def rss(request, **kwargs):
    """Shows the details for a BlogEntry entity (instance of)"""
    db = request.environ['schevo.db.zodb']
    k,messageid = base64.urlsafe_b64decode(kwargs['oid'].encode('utf8')).split(b':')
    obj = db.Message.findone(messageid=messageid)
    
    # fetch the related comments for this post
    if not obj:
        raise HTTPNotFound("no such object!!!")

    xml = PyRSS2Gen.RSS2(
        title=obj.content,
        link=url_for(request.environ, obj.get_absolute_url()),
        description=obj.content
        )

    if hasattr(obj.x, 'comments'):
        for comment in obj.x.comments():
            xml.items.append(PyRSS2Gen.RSSItem(
                title=comment.sender_message,
                link=url_for(request.environ, comment.path_url)
                ))
    return HTTPResponse(xml.to_xml(), mimetype='text/xml')
