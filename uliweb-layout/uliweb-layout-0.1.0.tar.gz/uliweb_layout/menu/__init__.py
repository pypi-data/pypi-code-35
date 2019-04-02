from __future__ import print_function, absolute_import, unicode_literals
__version__ = '1.0'
__url__ = ''
__author__ = 'limodou'
__email__ = 'limodou@gmail.com'

import os
from copy import deepcopy
from uliweb.utils.sorteddict import SortedDict
from uliweb.utils.common import import_attr
from uliweb.utils._compat import string_types, u

__menus__ = SortedDict()
__menu_items__ = {} #saving item to parent relation
_menu_order = 9000

class MenuException(Exception): pass

def load_menu(menus):
    """
    Load menu definitions
    """
    global __menus__, __menu_items__

    __menus__.clear()
    __menu_items__.clear()
    _m = []
    _menu_names = set() #each menu item should has unique name
    
    def _iter_menus(m, parent=''):
        """
        make menu tree to plat list
        """
        global _menu_order

        for i in m:
            _p = i.get('parent') or parent
            #if no order existed, then use defined order by default
            _m.append((_p, i.get('order', _menu_order), i))
            _menu_order += 1
            name = i['name']
            subs = i.get('subs', [])
            _iter_menus(subs, os.path.join(parent, name).replace('\\', '/'))
            i['subs'] = []
    
    def _f(menus):
        for name, item in menus:
            x = deepcopy(item)
            x['name'] = name
            yield x
    
    _iter_menus(_f(menus))

    _m.sort()

    #rebuild menu tree
    stack = [('', None)]
    while len(stack) > 0:
        parent, pitem = stack.pop(0)
        i = 0
        find = False
        while i<len(_m):
            _p, _, mitem = _m[i]
            is_path = '/' in _p
            if _p == parent or (is_path and pitem and pitem.get('id').endswith(_p)):
                name = mitem['name']
                if not parent:
                    __menus__[name] = mitem
                    _id = name
                else:
                    pitem['subs'].append(mitem)
                    _id = pitem.get('id') + '/' + name
                mitem['id'] = _id
                __menu_items__[name] = _p
                stack.append((name, mitem))
                find = True
                _m.pop(i)
            else:
                if find:
                    break
                i += 1
    return __menus__

def get_menu(name):
    global __menus__

    assert name
    
    path = name.split('/')
    items = __menus__[path[0]]
    if len(path) > 1:
        _items = items
        find = False
        for p in path[1:]:
            for x in _items.get('subs', []):
                if p == x.get('name'):
                    _items = x
                    find = True
                    break
        if find:
            items = _items
        else:
            raise KeyError("Can't find menu item %s" % name)
        
    return items
    
def print_menu(root=None, title=False, verbose=False):
    global __menus__
    
    items = __menus__
    if root:
        items = get_menu(root)
    
    def p(menus, tab=0):
        print (' '*tab + menus['name'], end='')
        if title or verbose:
            txt = '[' + menus.get('title', menus['name']) + ']'
        else:
            txt = ''
        if verbose:
            d = SortedDict()
            for x in ['id', 'link']:
                if menus.get(x):
                    d[x] = menus.get(x)
            txt += ' {%s}' % (','.join(['%s="%s"' % (x, y) for x, y in d.items()]))
        print (txt)
        for x in menus.get('subs', []):
            p(x, tab+4)
       
    if not root:
        for x in items.values():
            p(x)
    else:
        p(items)
            
def after_init_apps(sender):
    from uliweb import settings
    
    load_menu(settings.MENUS.items())
    
def default_validators(item, context):
    """
    Check role and permission
    role and permission check result will be cached in context dict
    """
    from uliweb import functions, request
    
    roles = item.get('roles', [])
    perms = item.get('permissions', [])
    if roles or perms:
        if roles:
            con_roles = context.setdefault('roles', {})
            for x in roles:
                if x in con_roles:
                    flag = con_roles[x]
                else:
                    flag = functions.has_role(request.user, x)
                    con_roles[x] = flag
                if flag:
                    return flag
            
        if perms:
            con_perms = context.setdefault('permissions', {})
            for x in perms:
                if x in con_perms:
                    flag = con_perms[x]
                else:
                    flag = functions.has_permission(request.user, x)
                    con_perms[x] = flag
            if flag:
                return flag
    else:
        return True
    
def _validate(menu, context, validators=None):
    #validate permission
    validators = validators or []
    
    check = menu.get('check')
    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    
    validators = validators + check
    
    if validators:
        flag = False
        for v in validators:
            if not v: continue
            if isinstance(v, string_types):
                func = import_attr(v)
            else:
                func = v
            flag = func(menu, context)
            if flag:
                flag = True
                break
    else:
        flag = True
        
    return flag
    
def navigation(name, active='', check=None, id=None, _class=None):
    from uliweb import settings
    
    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    validators = (settings.MENUS_CONFIG.validators or []) + list(check)
    
    _navigation = settings.MENUS_CONFIG.navigation_render or default_navigation
    return import_attr(_navigation)(name=name, active=active, validators=validators, id=id, _class=_class)

def menu(name, active='', check=None, id=None, _class=None):
    from uliweb import settings

    if check and not isinstance(check, (list, tuple)):
        check = [check]
    else:
        check = []
    validators = (settings.MENUS_CONFIG.validators or []) + list(check)
    
    _menu = settings.MENUS_CONFIG.menu_render or default_menu
    return import_attr(_menu)(name=name, active=active, validators=validators, id=id, _class=_class)

def iter_menu(name, active='', validators=None):
    x = active.split('/')
    items = get_menu(name)
    context = {}
    
    def p(menus, active, index=0):
        
        begin = False
        
        #process sub menus
        for j in menus.get('subs', []):
            flag = _validate(j, context, validators)

            if index < len(x):
                _name = x[index]
            else:
                _name = ''

            _active = _name == j['id'].split('/')[-1]

            link = j.get('link', '#')
            title = j.get('title', j['name'])
            expand = j.get('expand', False)

            d = j.copy()
            d.update({'active':_active, 'title':title, 'link':link,
                      'expand':expand, 'index':index, 'name':j['name']})

            if not flag:
                continue
            
            if not begin:
                yield 'begin', d
                begin = True
                
            yield 'open', d
            
            yield 'item', d
            
            for y in p(j, active, index+1):
                yield y
            
            yield 'close', {'index':index+1}
        
        if begin:
            yield 'end', d
         
    for m in p(items, active):
        yield m
    
def default_menu(name, active='', validators=None, id=None, _class=None,
                 menu_default_class='sidebar-menu'):
    """
    :param menu: menu item name
    :param active: something like "z"
    :param check: validate callback, basic validate is defined in settings
    """
    from uliweb.utils.common import safe_unicode

    if active and '/' not in active:
        active = '/'.join(__menu_items__[active].split('/')[1:] + [active])

    s = []
    for _t, y in iter_menu(name, active, validators):
        index = y['index']
        indent = ' '*index*2
        if _t == 'item':
            _lica = []
            if y['active']:
                _lica.append('active')
            if y['expand']:
                _lica.append('open')
            if y['subs']:
                _lica.append("treeview")
            _licstr = 'class="%s"' % (' '.join(_lica)) if _lica else ''
            _name = ' name="%s"' % y['name']
            s.extend([indent, '<li ', _licstr, _name, '><a href="', y['link'], '">'])
            if 'icon' in y and y['icon']:
                if y['icon'].startswith("ion-"):
                    s.extend(['<i class="ion %s"></i>' % y['icon']])
                elif y['icon'].startswith("fa-"):
                    s.extend(['<i class="fa %s"></i>' % y['icon']])
                else:
                    s.extend(['<i class="fa fa-%s"></i>' % y['icon']])
            else:
                if index > 1:
                    s.append('<i class="fa fa-angle-double-right"></i>')


            s.extend([indent, '<span>', safe_unicode(y['title']), '</span>'])
            if y['subs']:
                s.append('<i class="fa fa-angle-left pull-right"></i>')
            s.append('</a>')
        elif _t == 'open':
            pass
        elif _t == 'close':
            s.append('</li>\n')
        elif _t == 'begin':
            if index == 0:
                _id = (' id="%s"' % id) if id else ''
                _cls = (' %s' % _class) if _class else ''
                s.append('<ul class="%s %s"%s>\n' % (menu_default_class, _cls, _id))
            else:
                s.extend(['\n', indent, '<ul class="treeview-menu">\n'])
        else:
            s.extend([indent, '</ul>\n', indent])

    return ''.join(s)

def default_navigation(name, active='', validators=None, id=None, _class=None,
                 menu_default_class='nav navbar-nav'):
    """
    :param menu: menu item name
    :param active: something like "x/y/z"
    :param check: validate callback, basic validate is defined in settings
    """
    from uliweb.utils.common import safe_unicode

    s = []
    for _t, y in iter_menu(name, active, validators):
        index = y['index']
        indent = ' '*index*2
        if _t == 'item':
            _lica = []
            if y['active']:
                _lica.append('active')
            # if y['expand']:
            #     _lica.append('open')
            # if y['subs']:
            #     s.extend([indent, '<li class="dropdown">'])
            #     s.extend([indent, '<a href="#" class="dropdown-toggle" data-toggle="dropdown">{} <span class="caret"></span></a>'.format(safe_unicode(y['title']))])
            # else:

            _licstr = 'class="%s"' % (' '.join(_lica)) if _lica else ''
            _name = ' name="%s"' % y['name']
            if y['subs']:
                s.extend(['\n', indent, '<li class="dropdown">'])
                s.extend(['\n', indent, u'<a href="#" class="dropdown-toggle" data-toggle="dropdown">{} <span class="caret"></span></a>'.format(safe_unicode(y['title']))])
                s.extend(['\n', indent, '<ul class="dropdown-menu">\n'])
            else:
                s.extend([indent, '<li ', _licstr, _name, '><a href="', y['link'], '">'])
                # remove icon
                # if 'icon' in y and y['icon']:
                #     if y['icon'].startswith("ion-"):
                #         s.extend(['<i class="ion %s"></i>' % y['icon']])
                #     elif y['icon'].startswith("fa-"):
                #         s.extend(['<i class="fa %s"></i>' % y['icon']])
                #     else:
                #         s.extend(['<i class="fa fa-%s"></i>' % y['icon']])
                # else:
                if index > 1:
                    s.append('<i class="fa fa-angle-double-right"></i>')


                s.extend([safe_unicode(y['title'])])
                s.append('</a>')
        elif _t == 'open':
            pass
        elif _t == 'close':
            s.append('</li>\n')
        elif _t == 'begin':
            if index == 0:
                _id = (' id="%s"' % id) if id else ''
                _cls = (' %s' % _class) if _class else ''
                s.append('<ul class="%s %s"%s>\n' % (menu_default_class, _cls, _id))
            # else:
            #     s.extend(['\n', indent, '<li class="dropdown">'])
            #     s.extend(['\n', indent, '<a href="#" class="dropdown-toggle" data-toggle="dropdown">{}</a>'.format(safe_unicode(y['title']))])
            #     s.extend(['\n', indent, '<ul class="dropdown-menu">\n'])
        else:
            s.extend([indent, '</ul>\n', indent])

    return ''.join(s)

def print_menu_html(name, type='side'):
    from uliweb import settings

    if type == 'side':
        _menu = settings.MENUS_CONFIG.menu_render or default_menu
    elif type == 'main':
        _menu = settings.MENUS_CONFIG.menu_render or default_navigation
    print (import_attr(_menu)(name=name))

def mainmenu(*active):
    from uliweb import settings

    return navigation('MAINMENU', *active)

def sidemenu(menuname, *active):
    from uliweb import settings

    return menu(menuname, *active)

def startup_installed(sender):
    from uliweb.core import template

    template.default_namespace['mainmenu'] = mainmenu
    template.default_namespace['sidemenu'] = sidemenu

def breadcrumb(menu, active, suffix='', prefix=''):
    """
    Output breadcrumb html code
    :param menu: menu name
    :param active: active menu item name
    :param suffix: string append to breadcrumb
    :return: string(html code)
    """
    from uliweb.utils.common import safe_str

    items = get_menu(menu).get('subs', [])
    if '/' not in active:
        active = '/'.join(__menu_items__[active].split('/')[1:] + [active])
    path = active.split('/')

    def _iter_item(menus):
        for c in path:
            for item in menus:
                if item['name'] == c:
                    menus = item.get('subs', [])
                    yield item
                    break

    s = ['<ol class="breadcrumb">']
    for i, p in enumerate(_iter_item(items)):
        if prefix and i==0:
            s.append('<li>{}</li>'.format(u(prefix)))
        if i == len(path) - 1:
            s.append('<li><a href="{}">{}</a></li>'.format(p.get('link', '#'), u(p.get('title'))))
            if suffix:
                s.append('<li>{}</li>'.format(u(suffix)))
        else:
            s.append('<li><a href="{}">{}</a></li>'.format(p.get('link', '#'), u(p.get('title'))))
    s.append('</ol>')
    return '\n'.join(s)
