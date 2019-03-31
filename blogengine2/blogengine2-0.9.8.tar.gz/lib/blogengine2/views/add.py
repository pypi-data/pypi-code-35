#!/usr/bin/env python
# All rights reserved.
# Please see the "LICENSE" file for license details.
"""Management views"""

import os
import random
import logging
log = logging.getLogger(__name__)

from notmm.dbapi.orm import decorators
from notmm.utils.wsgilib import HTTPUnauthorized, HTTPRedirectResponse
from notmm.utils.template import direct_to_template
from notmm.utils.django_settings import LazySettings

from blogengine2.contrib.comments import CommentForm
from blogengine2.config import RemoteUser, UserIn
from blogengine2.contrib.api_v1 import EntryForm, AuthorManager, CategoryManager

from authkit.authorize.decorators import authorize

settings = LazySettings()

@authorize(UserIn(users=settings.ALLOWED_USERS))
@decorators.with_schevo_database('127.0.0.1:4545')
def add(request, template_name="blogengine2/api/add.mako", vote_disabled=True):

    db = request.environ['schevo.db.zodb'] # schevo.db.blogengine
    form = EntryForm(db)
    ctx = {'form': form}

    if request.method == 'POST':
        #handle POST request
        new_data = request.POST.copy()
        form = EntryForm(db, data=new_data)
        if form.is_valid():
            # Continue with schevo model validation
            tx_data = form.cleaned_data.copy()
            tx = db.Message.t.create()
            
            category = tx_data['category']

            tx.category = CategoryManager(connection=db).find_or_create(
                name=category)

            tx.messageid = random.randint(1, 5000)
            tx.content = tx_data['content']

            if request.user is not None:
                # find or create
                log.debug("checking if user %s exists..." % request.user)
                tx.author = AuthorManager(connection=db).find_or_create(username=request.user)
            else:
                # XXX redirect to /session_login/
                #return HTTPRedirectResponse('/session_login/')
                handle500 = request.environ['django.request.handle500']
                return handle500(request)

            #if not vote_disabled:
            #	message = db.Message.findone(messageid=messageid)
            #	vote = db.Vote.t.create(voteid=messageid,message=message)
            #	tx.count = 0 # initialize the counter
            db.execute(tx)
            return HTTPRedirectResponse('/blog/')
        else:
            log.debug(form.errors)
            ctx['form'] = form
    return direct_to_template(request, template_name, extra_context=ctx)
