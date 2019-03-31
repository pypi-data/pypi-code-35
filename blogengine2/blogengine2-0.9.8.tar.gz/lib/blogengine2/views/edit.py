#!/usr/bin/env python
# Copyright (c) 2009-2019 Etienne Robillard <tkadm30@yandex.com>
# All rights reserved.
# Please see the "LICENSE" file for license details. 
import base64

from notmm.utils.wsgilib import HTTPClientError, HTTPRedirectResponse
from notmm.dbapi.orm import decorators
from notmm.utils.django_settings import LazySettings
from notmm.utils.template import direct_to_template

from blogengine2.config import authorize, UserIn
from blogengine2.contrib.api_v1.forms import EntryForm

settings = LazySettings()

@authorize(UserIn(users=settings.ALLOWED_USERS))
@decorators.with_schevo_database('127.0.0.1:4545')
def edit(request, template_name="blogengine2/api/edit.mako"):
    
    # Initial template dict
    ctx = {}
    handle404 = request.environ['django.request.handle404']

    oid = request.query_args.get('oid')
    if oid is None:
        return handle404(request)
    
    # Get the current zodb database
    db = request.environ['schevo.db.zodb'] # schevo.db.blogengine
    #handle500 = request.environ['django.request.handle500']

    # Get the messageid
    k,messageid = base64.urlsafe_b64decode(oid.encode('utf8')).split(b':')
    # Retrieve the object (entity) using the given messageid
    obj = db.Message.findone(messageid=messageid)
    datadict = obj.s.field_map()
    form = EntryForm(db, data=datadict.value_map())
    ctx['form'] = form
    ctx['oid'] = obj._oid
    ctx['title'] = obj.content
    if request.method == 'POST':
        #handle POST request
        new_data = request.POST.copy()
        form = EntryForm(db, data=new_data)
        if form.is_valid():
            # Continue with schevo model validation
            obj = db.Message.findone(messageid=obj._oid)
            tx = obj.t.update(**form.cleaned_data)
            db.execute(tx)  # execute the transaction/commit
            db.commit() # object saved
            return HTTPRedirectResponse(obj.get_absolute_url())
    return direct_to_template(request, template_name, extra_context=ctx)
