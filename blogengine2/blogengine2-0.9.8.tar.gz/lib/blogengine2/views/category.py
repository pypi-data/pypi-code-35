#!/usr/bin/env python
# coding: UTF-8
import os, random

from notmm.dbapi.orm import decorators
from notmm.utils.template import direct_to_template
from notmm.utils.wsgilib.exc import HTTPUnauthorized, HTTPRedirectResponse
from notmm.utils.django_settings import LazySettings

from blogengine2.contrib.comments import CommentForm
from blogengine2.config import UserIn, authorize
from blogengine2.contrib.api_v1.forms import CategoryForm


settings = LazySettings()

@decorators.with_schevo_database('127.0.0.1:4545')
def details(request, slug, template_name="blogengine2/category_detail.mako", **kwargs):
    db = request.environ['schevo.db.zodb']
    # woot :)
    handle500 = request.environ['django.request.handle500'] 
    handle404 = request.environ['django.request.handle404']

    ctx = {}
    try:
        obj = db.Category.findone(slug=slug)
        if obj is not None:
            ctx['category'] = obj
            return direct_to_template(request, template_name, extra_context=ctx)
    except Exception:
        # create the category form 
        return handle500(request)
    return handle404(request)

@decorators.with_schevo_database('127.0.0.1:4545')
def index(request, template_name="blogengine2/categories.mako", **kwargs):
    db = request.environ['schevo.db.zodb']
    categories = db.Category.find()
    #print [x.name for x in categories]
    ctx = {
        'categories' : [item for item in categories]
        }
    return direct_to_template(request, template_name, extra_context=ctx)

###
### Admin views.
###
@authorize(UserIn(users=settings.ALLOWED_USERS))
@decorators.with_schevo_database('127.0.0.1:4545')
def add(request, template_name="blogengine2/category_add.mako", **kwargs):
    form = CategoryForm()
    ctx = {
        'form'    : form,
        'request' : request
        #'message' : 'Use the form below to create a new category.'
    }
    if request.method == 'POST':
        #handle POST request
        new_data = request.POST.copy()
        #print new_data
        form = CategoryForm(new_data)
        if form.is_valid():
            # Continue with schevo model validation
            cleaned_data = form.cleaned_data
            db = request.environ['schevo.db.zodb'] # schevo.db.blogengine
            tx = db.Category.t.create(**cleaned_data)  # create the schevo transaction object
            if tx is not None:
                db.execute(tx)  # execute the transaction/commit
                #db.commit()

            return HTTPRedirectResponse('/')
        else:
            ctx['form'] = form
            ctx['message'] = 'Error saving the new data. Please try again.'

    return direct_to_template(request, template_name, extra_context=ctx)
