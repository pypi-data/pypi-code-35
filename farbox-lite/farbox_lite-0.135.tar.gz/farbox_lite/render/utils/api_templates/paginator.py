#coding: utf8
from __future__ import absolute_import

paginator = u"""{% set paginator_style = paginator_style or 'simple' %}

{% set paginator_css_class = 'paginator pager pagination' %}
{% if  not paginator.has_pre and not paginator.has_next %}
{% set paginator_css_class = paginator_css_class + " no_pages" %}

{% endif %}
<div class="{{paginator_css_class}}" >
  <div class="paginator_container pagination_container">{% if  paginator.has_pre or paginator.has_next %}{% if  paginator_style == 'auto' %}{% if  max_count %}{{ paginator.set_default_max_page_numbers(max_count) }}

{% endif %}
{% set omission_mark = omission_mark or '...' %}
{% for page_number in paginator.page_numbers %}{% if  page_number %}
{% set is_current = True if paginator.page==page_number else False %}
<a href="{{paginator.get_page_url(page_number)}}"  class="{{'current' if is_current else ''}}" >{{ page_number }}</a>

{% else %}<span class="fill">{{ omission_mark }}</span>

{% endif %}

{% endfor %}
{% elif  paginator_style == 'mini' %}
{% set max_count = max_count or 5 %}
{% if  max_count < 3 %}
{% set max_count = 3 %}

{% endif %}{% if  max_count > 20 %}
{% set max_count = 20 %}

{% endif %}
{% set middle_count = (max_count/2).int %}
{% if  paginator.page <= middle_count %}
{% set page_begin = 1 %}

{% else %}
{% set page_begin = paginator.page - middle_count %}

{% endif %}
{% if  paginator.page + middle_count + 1 > paginator.total_pages %}
{% set page_end = paginator.total_pages + 1 %}

{% else %}
{% set page_end = paginator.page + middle_count + 1 %}

{% endif %}
{% if  paginator.has_pre %}<a href="{{paginator.pre_page_url}}"  rel="prev" class="prev">{{ pre_label }}</a>

{% endif %}{% for page in range(page_begin, page_end) %}
{% set a_class = 'page-number current' if page==paginator.page else 'page-number' %}
<a href="{{paginator.get_page_url(page)}}"  class="{{a_class}}" >{{ page }}</a>

{% endfor %}{% if  paginator.has_next %}<a href="{{paginator.next_page_url}}"  rel="next" class="next">{{ next_label }}</a>

{% endif %}
{% else %}{% if  paginator.has_pre %}<a href="{{paginator.pre_url}}"  class="btn pre newer-posts newer_posts">{{ pre_label }}</a>

{% endif %}{% if  show_page_of %}<span class="page_number page-number">{{ 'Page %s of %s' % (paginator.page, paginator.pages) }}</span>

{% endif %}{% if  paginator.has_next %}<a href="{{paginator.next_url}}"  class="btn next older-posts older_posts">{{ next_label }}</a>

{% endif %}
{% endif %}

    <div style="clear:both;height:0;"></div>

{% endif %}
  </div>

</div>"""