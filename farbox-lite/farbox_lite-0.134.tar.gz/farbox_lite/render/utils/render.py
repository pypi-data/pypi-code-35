#coding: utf8
from __future__ import absolute_import
from farbox_lite.template_system.env import farbox_lite_env
from farbox_lite.render.utils import api_templates



def render_template_source(template_source, *args, **kwargs):
    if not template_source:
        return ''
    try:
        template = farbox_lite_env.from_string(template_source)
        html_content = template.render(*args, **kwargs)
    except:
        html_content = '<div style="color:red">api template error</div>'
    return html_content



def render_api_template(name, *args, **kwargs):
    template_source = getattr(api_templates, name, '')
    return render_template_source(template_source, *args, **kwargs)
