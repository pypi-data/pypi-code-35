from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import Library
from django.template.loader import render_to_string
from django.utils.translation import get_language

from ..models import MetaData

register = Library()

try:
    from constance import config
except ImportError:
    config = None


@register.simple_tag(takes_context=True)
def get_meta(context, obj):
    lang_code = get_language()
    content_type = ContentType.objects.get_for_model(obj)
    title_field_name = getattr(obj, 'title_field_name', 'title')
    ctx = {'request': context['request'], 'title': getattr(obj, title_field_name, None)}
    try:
        meta = MetaData.objects.get(content_type=content_type, object_id=obj.id)
        for attr in ['description', 'keywords', 'author', 'robots', 'title']:
            ctx[attr] = getattr(meta, attr) or ctx.get(attr)
    except MetaData.DoesNotExist:
        pass

    if hasattr(obj, 'get_meta_title'):
        ctx['title'] = obj.get_meta_title()

    if hasattr(obj, 'get_meta_keywords'):
        ctx['keywords'] = obj.get_meta_keywords()

    if hasattr(obj, 'get_meta_description'):
        ctx['description'] = obj.get_meta_description()

    if config:
        for attr in ['description', 'keywords', 'author', 'robots']:
            ctx[attr] = ctx.get(attr) or \
                        getattr(config, ('dseo_default_%s' % attr).upper(), '') or \
                        getattr(config, ('dseo_default_%s_%s' % (attr, lang_code)).upper(), '')

        prefix = getattr(config, 'DSEO_META_TITLE_PREFIX', '') or \
                 getattr(config, ('dseo_meta_title_prefix_%s' % lang_code).upper(), '')
        if prefix and not getattr(obj, 'is_home_page', False):
            ctx['title'] = prefix + ' ' + ctx['title']

        postfix = getattr(config, 'DSEO_META_TITLE_POSTFIX', '') or \
                  getattr(config, ('dseo_meta_title_postfix_%s' % lang_code).upper(), '')
        if postfix and not getattr(obj, 'is_home_page', False):
            ctx['title'] = ctx['title'] + ' ' + postfix

    return render_to_string('templatetags/meta.html', ctx)
