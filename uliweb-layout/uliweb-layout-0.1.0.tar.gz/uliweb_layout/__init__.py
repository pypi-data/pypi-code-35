__version__ = '0.1.0'
__url__ = 'https://github.com/uliwebext/uliweb-layout'
__author__ = 'limodou'
__email__ = 'limodou@gmail.com'
__license__ = 'BSD'

from io import StringIO
from uliweb.utils.common import safe_str


class LayoutUtils(object):
    def theme(self):
        return get_current_theme()

    def submenu(self, menus, *actives):
        return self.left_side_menu(menus, True, 1, *actives)

    def uliweb_layout_sidebar_menu(self, menus, *actives):
        return self.left_side_menu(menus, True, 1, *actives)

    def left_side_menu(self, menu_items, is_folder, level, *actives):
        from uliweb.utils.common import safe_str

        if len(actives) > 0:
            active = actives[0]
            items = actives[1:]
        else:
            active = None
            items = ()
        out = StringIO()
        if is_folder:
            out.write("<ul class='sidebar-menu'>")
        else:
            out.write("<ul class='treeview-menu'>")
        for x in menu_items:
            if active == x['name']:
                li_class = "active"
            else:
                li_class = ""
            if is_folder:
                li_class = "treeview " + li_class
                sub_icon = "<i class=\"fa fa-link\"></i>"
            else:
                sub_icon = ""
            if x.get('subs', None):
                link = "#"
                target = '_self'
                out.write(
                    '<li class=\"%s\"><a href=\"%s\" target=\"%s\">%s<span>%s</span><i class=\"fa fa-angle-left pull-right\"></i></a>' % (
                    li_class, link, target,sub_icon, safe_str(x["title"])))
            else:
                link = x.get("link", "#")
                target = x.get('target', '_self')
                out.write(
                    '<li class=\"%s\"><a href=\"%s\" target=\"%s\">%s<span>%s</span></a>' % (
                    li_class, link, target,sub_icon, safe_str(x["title"])))

            if x.get('subs', None):
                out.write(self.left_side_menu(x['subs'], False, level + 1, *items))
            out.write("</li>")
        out.write("</ul>")
        return out.getvalue()

def get_layout_utils():
    utils = LayoutUtils()
    return utils


def get_current_theme():
    from uliweb import settings

    return settings.THEME.CURR_THEME
