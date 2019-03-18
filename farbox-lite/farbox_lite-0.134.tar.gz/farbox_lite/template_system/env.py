#coding: utf8
from __future__ import absolute_import
from farbox_lite.utils import to_unicode, get_md5
from jinja2.loaders import  BaseLoader
from jinja2.environment import Template
from jinja2.utils import internalcode
from jinja2.exceptions import TemplateNotFound
from jinja2 import sandbox
import os

from farbox_lite.compiler.templates import update_template_resources
from farbox_lite.template_system.utils import SafeUndefined, Undefined
from farbox_lite.render.apis.site import get_site_from_request
from farbox_lite.template_system.monkey.attr import env_call, env_getattr, env_handle_exception


def return_error_message(message):
    if 'error_ignored' in message:
        error_info = ''
    else:
        error_info = '<span style="color:red" class="template_api_error">&lt;%s&gt:</span>' % message
    return error_info




def get_template_source(template_name, hit_newest=True):
    site = get_site_from_request()
    if not site:
        return
    site_root = site['filepath']
    template_resources = site.get('template_resources')
    if not template_resources or not isinstance(template_resources, dict):
        return

    template_resource_mtimes = template_resources.get('_')
    if not isinstance(template_resource_mtimes, dict):
        template_resource_mtimes = {}

    template_name = template_name.strip('"\'').strip('/').lower()
    if not template_name: # 首页
        template_name = 'index.html'
    if template_name.endswith('.jade'):
        template_name = template_name.replace('.jade', '.html')
    if not template_name.endswith('.html'): # 比如 import a.b
        template_name = template_name.replace('.', '/')
        template_name += '.html'

    source = ''
    template_name_to_hit = None
    template_name_parts = os.path.splitext(template_name)[0].split('/')
    for length in range(len(template_name_parts), 0, -1):
        template_name_to_hit = '/'.join(template_name_parts[:length]) + '.html'
        if template_name_to_hit in template_resources:
            source = to_unicode(template_resources.get(template_name_to_hit))
            break

    if hit_newest and source and template_name_to_hit:
        template_resource_mtime_info = template_resource_mtimes.get(template_name_to_hit)
        if template_resource_mtime_info:
            template_filepath, mtime = template_resource_mtime_info
            if os.path.isfile(template_filepath):
                new_mtime = os.path.getmtime(template_filepath)
                if new_mtime != mtime:
                    site['template_resources'] = update_template_resources(site_root)
                    return get_template_source(template_name, hit_newest=False)

    # at last
    return source


class FarboxLiteTemplateLoader(BaseLoader):
    def get_source(self, environment, template_name):
        template_source = get_template_source(template_name)
        if template_source:
            return template_source, template_name, lambda: True
        else:
            raise TemplateNotFound(template_name)

    @internalcode
    def load(self, environment, name, globals=None):
        globals = globals or {}
        source, filename, uptodate = self.get_source(environment, name)
        code = environment.compile(source, name, filename)
        template = environment.template_class.from_code(environment, code, globals, uptodate)
        template.source = source
        return template




class FarboxLiteEnvironment(sandbox.SandboxedEnvironment): #  Environment
    intercepted_binops = frozenset(['**', '*', '/', '+'])
    def __init__(self, *args, **kwargs):
        kwargs['autoescape'] = False
        kwargs['auto_reload'] = False
        kwargs['cache_size'] = 50000
        kwargs['extensions'] = ['jinja2.ext.do']
        super(FarboxLiteEnvironment, self).__init__(*args, **kwargs)
        self.undefined = SafeUndefined
        self.loader =  FarboxLiteTemplateLoader()

    @staticmethod
    def template_not_found(name):
        content = return_error_message("template error: can't find the template named `%s`" % name)
        return Template(content)

    def get_template(self, name, parent=None, globals=None):
        if isinstance(name, Template):
            return name
        globals = self.make_globals(globals)

        is_parent = bool(not parent)

        template_source = get_template_source(name)
        if template_source:
            template_md5_key = get_md5(template_source)
            template = self.cache.get(template_md5_key)
            if template is None:
                template = self.loader.load(environment=self, name=name, globals=globals)
                self.cache[template_md5_key] = template
            return template
        else:
            if is_parent:
                raise TemplateNotFound(name)
            else:
                return self.template_not_found(name)


    def getattr(self, obj, attribute):
        if isinstance(obj, Undefined):
            return SafeUndefined()
        return env_getattr(self, obj, attribute, sandbox=True)


    def call(self, context, context_obj, *args, **kwargs):
        """Call an object from sandboxed code."""
        # the double prefixes are to avoid double keyword argument
        # errors when proxying the call.
        return env_call(self, context, context_obj, *args, **kwargs)


    def handle_exception(self, exc_info=None, rendered=False, source_hint=None):
        return env_handle_exception(self, exc_info, rendered, source_hint)


farbox_lite_env = FarboxLiteEnvironment()
