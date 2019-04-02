from uliweb.utils.generic import DetailTableLayout

class Bootstrap3DetailTableLayout(DetailTableLayout):
    default_class = 'view-bs3-table'
    default_table_class = ''
    default_title_class = "box-primary"


    def __init__(self, layout, get_field, model=None, table_class=None, title_class=None, **kwargs):
        self.layout = layout
        self.get_field = get_field
        self.model = model
        self.table_class = table_class or self.default_table_class
        self.title_class = title_class or self.default_title_class
        self.kwargs = kwargs

    def line(self, fields, n):
        from uliweb.core.html import Tag

        _x = 0
        for _f in fields:
            if isinstance(_f, (str, unicode)):
                _x += 1
            elif isinstance(_f, dict):
                _x += _f.get('colspan', 1)
            else:
                raise Exception('Colume definition is not right, only support string or dict')

        tr = Tag('tr')
        with tr:
            for x in fields:
                _span = n / _x
                if isinstance(x, (str, unicode)):
                    f = self.get_field(x)
                elif isinstance(x, dict):
                    f = self.get_field(x['name'])
                    _span = _span * x.get('colspan', 1)

                with tr.td(colspan=_span, width='%d%%' % (100*_span/n,), _class='view-cell'):
                    with tr.div(_class='table-field-row', id='view_field_{}'.format(f['name'])):
                        with tr.label(_class='table-field-label'):
                            tr << f['label'] + ':'
                        if isinstance(x, dict) and x.get('break'):
                            tr << '<br/>'
                        with tr.div(_class='table-field-col'):
                            tr << f['display']

        return tr


    def render(self):
        from uliweb.core.html import Builder
        from uliweb.form.layout import min_times

        m = []
        for line in self.layout:
            if isinstance(line, (tuple, list)):
                _x = 0
                for f in line:
                    if isinstance(f, (str, unicode)):
                        _x += 1
                    elif isinstance(f, dict):
                        _x += f.get('colspan', 1)
                    else:
                        raise Exception('Colume definition is not right, only support string or dict')
                m.append(_x)
            else:
                m.append(1)
        n = min_times(m)

        buf = Builder('begin', 'body', 'end')
        table = None
        fieldset = None
        first = True
        for fields in self.layout:
            if not isinstance(fields, (tuple, list)):
                if isinstance(fields, (str, unicode)) and fields.startswith('--') and fields.endswith('--'):
                    # THis is a group line
                    if table:
                        buf.body << '</tbody></table></div></div>'
                    buf.body << '<div class="box {}">'.format(self.title_class)
                    title = fields[2:-2].strip()
                    if title:
                        buf.body << self.title(title)
                    buf.body << '<div class="box-body">'
                    buf.body << '<table class="{} {}"><tbody>'.format(self.table_class, self.default_class)
                    table = True
                    first = False
                    continue
                else:
                    fields = [fields]
            if first and not table:
                first = False
                buf.body << '<div class="box {}">'.format(self.title_class)
                buf.body << '<div class="box-body">'
                buf.body << '<table class="{} {}">'.format(self.table_class, self.default_class)
                buf.body << '<tbody>'
                table = True
            buf.body << self.line(fields, n)
        # close the tags
        if table:
            buf.body << '</tbody></table></div></div>'

        return buf


    def title(self, title=''):
        if title:
            return '''
<div class="box-header with-border"><h3 class="box-title">{}</h3>
  <div class="box-tools pull-right">
    <button type="button" class="btn btn-box-tool" data-widget="collapse" data-toggle="tooltip" title="" data-original-title="Collapse">
      <i class="fa fa-minus"></i>
    </button>
  </div>
</div>'''.format(title)
        return ''
