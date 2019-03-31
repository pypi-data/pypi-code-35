#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from notmm.controllers.auth     import AuthCookieController
from notmm.controllers.wsgi import WSGIController
from notmm.utils.django_settings import LazySettings


# init the django settings subsystem
settings = LazySettings()

__all__ = ['make_app']

def make_app(controller=WSGIController, enable_oauth=False):
    
    wsgi_app = controller(
        settings=settings,
        app_conf={'django.settings_autoload': True,
                  'logging.disabled': False}
    )
    if enable_oauth:
        from wsgi_oauth2 import client
        google_client = client.GoogleClient(
            settings.OAUTH2_CLIENT_ID,
            access_token=settings.OAUTH2_ACCESS_TOKEN,
            scope=settings.OAUTH2_SCOPE, 
            redirect_url=settings.OAUTH2_REDIRECT_URL)
        
        # see wsgi_oauth2.controller.OAuthController
        wsgi_app = google_client.wsgi_middleware(
            wsgi_app, client=google_client,
            secret=settings.SECRET_KEY, 
            login_path=settings.OAUTH2_LOGIN_URL,
            forbidden_passthrough=settings.OAUTH2_FORBIDDEN_PASSTHROUGH)
    return wsgi_app
