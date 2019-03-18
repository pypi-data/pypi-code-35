#coding: utf8
from __future__ import absolute_import
import re
from farbox_lite.utils import smart_unicode, UnicodeWithAttrs, make_content_clean
from farbox_lite.utils.functional import curry
from farbox_lite.utils.lazy import get_value_from_data, cut_content_by_words
from farbox_markdown.compile_md import fix_relative_image_path
import cgi

# backend也有用到,所以放在farbox.utils中

def html_escape(content):
    escaped_content = cgi.escape(content)
    escaped_content = make_content_clean(escaped_content)
    # escaped_content = escaped_content.replace('\x08', '').replace('\x07', '') # 去除 \a \b 标记
    return escaped_content

def linebreaks(value, post_path=None, render_markdown_image=False):
    """Converts newlines into <p> and <br />s."""
    # post_path 是处理图片本身的相对路径，这样就可以处理Markdown语法的图片了
    value = re.sub('<.*?[^>]$','', value) #避免尾行图片（源码）被截断
    value = re.sub(r'\r\n|\r|\n', '\n', value)
    paras = re.split('\n{2,}', value)
    new_paras = []
    for p in paras:
        p = "\n\n".join([u"<p>%s</p>"%line for line in re.split('\n',p)])
        p = u'<div class="p_part">%s</div>' %p
        new_paras.append(p)
    html = u'\n\n'.join(new_paras)
    if post_path or render_markdown_image:
        html = re.sub(r'!\[(.*?)\]\(([^")]+)\)', '<img title="\g<1>" src="\g<2>"/>', html) # 将Markdown  图片语法的转为 html
    if post_path:
        html = fix_relative_image_path(post_path, html) # 相对路径的图片需要进行转化
    return html




def html_to_text(content, keep_a_html=False, remove_a=True, keep_images=False, quote_tags=False):
    # keep_a_html 可以保留 a 元素 的完整逻辑
    # remove_a 表示整个A 元素删除，反之则是转为普通的文本
    content = re.sub(r'<!--.*?-->', '', content) # 先去除HTML的注释
    content = re.sub('<div class="linenodiv">.*?</div>', '', content, flags=re.S) # 去代码高亮
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.I|re.S)
    content = re.sub(r'</p>\s*<p>', '\n\n', content, flags=re.I|re.S)
    if keep_images:
        content = re.sub('(<img)([^<]+)(/?\s*>)', '&LT;img\g<2>/&GT;', content) # 保护图片代码

    if keep_a_html:
        remove_a = False
    if remove_a: # 会把 a 元素整体删除..
        content = re.sub(r'<a[^<]+>([^<]+)</a>', '', content, re.I|re.S)
    if keep_a_html: # 保留原始的 A 元素
        content = re.sub(r'(<)(a[^<]+)(>)([^<]+)(</a>)', '&LT;\g<2>&GT;\g<4>&LT;/a&GT;', content, re.I|re.S)

    content = re.sub(r'</?[^<]+?>', '', content).strip() # 去tag 标签
    #content = html_unescape(content)

    if quote_tags:
        content = content.replace('<', '&lt;').replace('>', '&gt;')


    # 还原 A  & IMG 元素
    content = content.replace('&LT;', '<').replace('&GT;', '>')


    content = re.sub(r'\n +', '\n', content)

    return content


HTML_C = re.compile(r'</?[^<]+?>')
def limit(content, length=None, mark='......', keep_images=True, words=None, post_path=None, remove_a=False, keep_a_html=False, ignore_first_tag_name=None):
    # like patch...
    # smartpage 中声明 css的
    # post_path 指定的，则会尝试解析 Markdown （插图）语法的逻辑
    content = re.sub('<div class="codehilite code_lang_css  highlight">.*?<!--block_code_end-->', '', content, flags=re.S)

    if ignore_first_tag_name:
        # 忽略掉首个 dom 元素，一般是 blockquote
        if isinstance(ignore_first_tag_name, (str, unicode)) and re.match(r'[a-z]+$', ignore_first_tag_name, re.I):
            content = content.strip()
            content = re.sub(r'^<%s[^<>]*>.*?</%s>'%(ignore_first_tag_name, ignore_first_tag_name), '', content, flags=re.I|re.S)

    if HTML_C.search(content): #如果有html的代码，则进行平文本转义
        content = html_to_text(content, keep_images=keep_images, remove_a=remove_a, keep_a_html=keep_a_html, quote_tags=True)
    if not length and not words: # 长度都没有说声明
        output = content
        has_more = False
    else:
        if words and isinstance(words, int):
            output = cut_content_by_words(content, words, mark=mark)
            has_more = getattr(output, 'has_more', False)
        else:
            output = content[0:length]
            if len(content) > length:
                has_more = True
                if mark:
                    output += smart_unicode(mark)
            else:
                has_more = False
    output = linebreaks(output, post_path=post_path)
    content = UnicodeWithAttrs(output)
    content.has_more = has_more
    content.without_pics = re.sub('<img[^<]+/\s*>', '', output) #去掉img节点
    content.without_pic = content.no_pic = content.without_pics

    return content





def replace_content_with_vars_by_re(value, re_obj):
    #all_matched = re_obj.group(0)
    key = re_obj.group(1)
    attrs = re_obj.group(2)
    if attrs: # 是属性的调用
        attrs = attrs.strip().strip('.')
        value = get_value_from_data(value, attrs)
    if value is None: value = ''
    value = smart_unicode(value)
    return value

def update_content_with_vars(content, data):
    # {{ var }}  的替换
    if not isinstance(data, dict):
        return content
    content = smart_unicode(content)
    content = content.replace('%7B%7B', '{{').replace('%7D%7D', '}}') # 转义
    for key, value in data.items():
        if re.match(r'[a-z0-9-_]+$', key): # key like comment, without dot, attr_call like comment.author
            content = re.sub(r'\{\{\s*(%s)([\w.]+)?\s*\}\}'% key, curry(replace_content_with_vars_by_re, value), content, flags=re.I)
    content = re.sub(r'\{\{\s*[\w.]+\s*\}\}', '', content) # 去除潜在未替换的变量
    return content



def get_images_from_html(content, relative_to_site=False):
    raw_images = re.findall("""<\s*img.*?src=['"]([^'"]+).*?>""", content, flags=re.I)
    images = []
    for image_src in raw_images:
        if image_src in images:
            continue
        if relative_to_site and ('://' in image_src or image_src.startswith('//')):
            continue
        images.append(image_src)
    return images


def _re_html_dom(html, rule):
    # 尝试对某些类型的 dom 元素的类型进行修改或者 wrap
    # h2: <section class=t1><section class=t2><section class=t3>$</section></section></section>\n
    # $ 表示作为 innerHTML， $$ 表示作为 outerHTML
    # 比如此列，$ 表示原来 h2 的innerHTML， 而 $$ 则是包括原始的整个h2
    if not isinstance(html, (str, unicode)):
        return html
    if not isinstance(rule, (list, tuple)) or len(rule)!=2:
        return html
    dom_type, dom_template = rule
    if not isinstance(dom_type, (str, unicode)) and not isinstance(dom_template, (str, unicode)): # ignore
        return html
    dom_type = dom_type.strip()
    if not re.match(r'[a-z0-9]{1,20}$', dom_type, flags=re.I): # 不符合dom type的类型，主要是避免产生正则的性能消耗
        return html
    matched_doms = re.findall(r'(<%s[^<>]*>(.*?)<\s*/%s\s*>)'%(dom_type, dom_type), html, re.S|re.M)
    for out_html, in_html in matched_doms:
        if '$$' in dom_template:
            new_dom_html = dom_template.replace('$$', in_html)
        else:
            new_dom_html = dom_template.replace('$', out_html)
        html = html.replace(out_html, new_dom_html)
    return html


def re_html_dom(html, rules):
    # 对_re_html_dom的增强，可以同时处理多个rules
    if not isinstance(rules, (list, tuple)):
        return html
    rules = rules[:100] # 最多进行100次的替换...不然性能实在太糟糕
    if len(rules) == 2: # 可能本身就是一个单一的 rule
        html = _re_html_dom(html, rules)
    for rule in rules:
        if not isinstance(rule, (list, tuple)):
            continue
        html = _re_html_dom(html, rule)
    return html