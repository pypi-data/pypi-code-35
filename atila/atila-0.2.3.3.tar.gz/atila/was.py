import os, sys
import time
from hmac import new as hmac
from hashlib import sha1
import base64
import pickle
import random
from rs4 import jwt
from aquests.protocols.http import http_date
from skitai import wsgiappservice 
from skitai.wastuff import futures
import skitai
from skitai.exceptions import HTTPError

class JWTUser:
    def __init__ (self, claims):
        self.__claims = claims
    
    @property
    def name (self):
        return self.__claims ["username"]
        
    def __getattr__ (self, attr):
        return self.__claims.get (attr)
            
    def __str__ (self):
        return self.name


class WAS (wsgiappservice.WAS):
    # mehiods remap ------------------------------------------------
    def __getattr__ (self, name):
        if self.in__dict__ ("app"): # atila app
            attr = self.app.create_on_demand (self, name)
            if attr:
                setattr (self, name, attr)
                return attr
        
        try:
            return self.objects [name]
        except KeyError:    
            raise AttributeError ("'was' hasn't attribute '%s'" % name)    
    
    # URL builders -------------------------------------------------
    def urlfor (self, thing, *args, **karg):
        # override with resource default args
        if not isinstance (thing, str) or thing.startswith ("/") or thing.find (":") == -1:
            return self.app.urlfor (thing, *args, **karg)        
        return self.apps.urlfor (thing, *args, **karg)    
    ab = urlfor
    
    def partial (self, thing, **karg):
        # override with current args
        karg ["__defaults__"] = self.request.args
        return self.ab (thing, **karg)
    
    def baseurl (self, thing):
        # resource path info without parameters
        return self.ab (thing, __resource_path_only__ = True)
    basepath = baseurl
    
    # event -------------------------------------------------    
    def broadcast (self, event, *args, **kargs):
        return self.apps.bus.emit (event, self, *args, **kargs)
    
    # JWT token --------------------------------------------------
    def mkjwt (self, claim, alg = "HS256"):
        assert "exp" in claim, "exp claim required"            
        return jwt.gen_token (self.app.salt, claim, alg)
        
    def dejwt (self, token = None):
        if not token:
            if self.request.JWT:            
                return self.request.JWT
            token_ = self.request.get_header ("authorization")
            if not token_ or token_ [:7].lower () != "bearer ":
                self.request.JWT = {"err": "no bearer token"}
                return self.request.JWT
            token = token_ [7:]
            
        try: 
            claims = jwt.get_claim (self.app.salt, token)
        except (TypeError, ValueError): 
            claims = {"err": "invalid token"}
        else:    
            if claims is None:
                claims = {"err": "invalid signature"}
            else:
                now = time.time ()
                if claims ["exp"] < now:
                    claims = {"err": "token expired"}
                elif "nbf" in claims and claims ["nbf"] > now:
                    claims = {"err": "token not activated yet"}

        self.request.JWT = claims    
        if "username" in claims:
            self.request.user = JWTUser (claims)        
        return claims
    
    # onetime token  ----------------------------------------
    def _unserialize_token (self, string):
        def adjust_padding (s):
            paddings = 4 - (len (s) % 4)
            if paddings != 4:
                s += ("=" * paddings)
            return s
        
        string = string.replace (" ", "+")
        try:
            base64_hash, data = string.split('?', 1)
        except ValueError:
            return    
        client_hash = base64.b64decode(adjust_padding (base64_hash))
        data = base64.b64decode(adjust_padding (data))
        mac = hmac (self.app.salt, None, sha1)        
        mac.update (data)
        if client_hash != mac.digest():
            return
        return pickle.loads (data)
    
    def mkott (self, obj, timeout = 1200, session_key = None):
        wrapper = {
            'object': obj,
            'timeout': time.time () + timeout
        }
        if session_key:
            token = hex (random.getrandbits (64))
            tokey = '_{}_token'.format (session_key)
            wrapper ['_session_token'] = (tokey, token)
            self.session.mount (session_key, session_timeout = timeout)
            self.session [tokey] = token
            self.session.mount ()            
            
        data = pickle.dumps (wrapper, 1)
        mac = hmac (self.app.salt, None, sha1)
        mac.update (data)
        return (base64.b64encode (mac.digest()).strip().rstrip (b'=') + b"?" + base64.b64encode (data).strip ().rstrip (b'=')).decode ("utf8")
    
    def deott (self, string):
        wrapper = self._unserialize_token (string)
        if not wrapper:
            return 
        
        # validation with session
        tokey = None
        has_error = False
        if wrapper ['timeout']  < time.time ():
            has_error = True
        if not has_error:
            session_token = wrapper.get ('_session_token')
            if session_token:
                # verify with session
                tokey, token = session_token                              
                self.session.mount (tokey [1:-6])
                if token != self.session.get (tokey):
                    has_error = True        
        if has_error:
            if tokey:
                del self.session [tokey]
                self.session.mount ()
            return
        
        self.session.mount ()
        obj = wrapper ['object']
        return obj
    
    def rvott (self, string):
        # revoke token
        wrapper = self._unserialize_token (string)
        session_token = wrapper.get ('_session_token')
        if not session_token:
            return
        tokey, token = session_token
        self.session.mount (tokey [1:-6])
        if not self.session.get (tokey):
            self.session.mount ()
            return
        del self.session [tokey]
        self.session.expire ()
        self.session.mount ()
    
    mktoken = token = mkott
    rmtoken = rvott
    detoken = deott
        
    # CSRF token ------------------------------------------------------    
    CSRF_NAME = "_csrf_token"
    @property
    def csrf_token (self):
        if self.CSRF_NAME not in self.session:
            self.session [self.CSRF_NAME] = hex (random.getrandbits (64))
        return self.session [self.CSRF_NAME]

    @property
    def csrf_token_input (self):
        return '<input type="hidden" name="{}" value="{}">'.format (self.CSRF_NAME, self.csrf_token)
    
    def csrf_verify (self, keep = False):
        if not self.request.args.get (self.CSRF_NAME):
            return False
        token = self.request.args [self.CSRF_NAME]
        if self.csrf_token == token:
            if not keep:
                del self.session [self.CSRF_NAME]
            return True
        return False
    
    # response shortcuts -----------------------------------------------
    REDIRECT_TEMPLATE =  (
        "<html><head><title>%s</title></head>"
        "<body><h1>%s</h1>"
        "This document may be found " 
        '<a HREF="%s">here</a></body></html>'
    )
    def redirect (self, url, status = "302 Object Moved", body = None, headers = None):
        redirect_headers = [
            ("Location", url), 
            ("Cache-Control", "max-age=0"), 
            ("Expires", http_date.build_http_date (time.time ()))
        ]
        if type (headers) is list:
            redirect_headers += headers
        if not body:
            body = self.REDIRECT_TEMPLATE % (status, status, url)            
        return self.response (status, body, redirect_headers)
        
    def render (self, template_file, _do_not_use_this_variable_name_ = {}, **karg):
        return self.app.render (self, template_file, _do_not_use_this_variable_name_, **karg)
    
    def API (self, *args, **karg):
        return self.response.API (*args, **karg)
    
    def Fault (self, *args, **karg):
        return self.response.Fault (*args, **karg)
    
    def File (self, *args, **karg):
        return self.response.File (*args, **karg)
    
    def Futures (self, reqs, timeout = 10):
        return futures.Futures (self._clone (True), reqs, timeout)
    futures = Futures
    
    @property
    def Error (self):
        return HTTPError
    
