#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 Etienne Robillard <tkadm30@yandex.com>
# All rights reserved.
# Please see the "LICENSE" file for license details. 
"""Details views"""
import logging, base64
log = logging.getLogger(__name__)

from notmm.dbapi.orm.decorators import with_schevo_database
from notmm.utils.template import RequestContext, direct_to_template

from blogengine2.contrib.comments import CommentForm
#from blogengine2.contrib.api_v1.model import MessageManager
#from blogengine2.config import authorize, RemoteUser
#from blogengine.config.global_settings import DATABASE_NAME

##@authorize(RemoteUser())
@with_schevo_database('127.0.0.1:4545')
def details(request, **kwargs):
    """Shows the details for a BlogEntry entity (instance of)"""

    db = request.environ['schevo.db.zodb']
    db._sync()

    handle500 = request.environ['django.request.handle500']

    #request.environ['schevo.db.default_manager'] = default_manager
    
    template_name = kwargs.pop('template_name', 
        'blogengine2/blogentry_detail.mako')
    
    if 'extra_context' in kwargs:
        params = kwargs['extra_context'].copy()
    else:
        params = {
            'comment_form' : CommentForm(),
            'oid' : kwargs['oid']}

    oid = params['oid'].encode('utf8')
    k,oid = base64.urlsafe_b64decode(oid).split(b':')
    
    try:
        result = db.Message.findone(messageid=oid)
    except Exception as exc:
        # invalid blog
        log.debug(exc)
        return handle500(request)

    params['blogentry'] = result # Hack
    #if not result:
    #    # invalid blog
    #    return handle404(request)

    if hasattr(result.x, 'votes'):
        votes = result.x.votes()
        if len(votes) >= 1:
            #assert len(votes) == 1
            vote_count = votes[0].count
        else:
            vote_count = 0
        params['vote_count'] = vote_count
    
    params['result'] = result
    params['path'] = result.get_absolute_url()
    # fetch the related comments for this post
    if hasattr(result.x, 'comments'):
        comments = result.x.comments()
        unpublished_comments = [item for item in comments if not item.x.is_published()]
        
        published_comments = set(comments).difference(unpublished_comments)
        
        # List of published (visible) comments
        params['comments'] = list(published_comments)
        # List of unpublished comments 
        params['u_comments_count'] = len(unpublished_comments)
    
    #params['request'] = request
    
    return direct_to_template(request, template_name, extra_context=params)
        
