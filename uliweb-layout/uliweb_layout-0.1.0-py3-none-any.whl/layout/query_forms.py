from uliweb import form
from uliweb.form.layout import QueryLayout

class NewQueryLayout(QueryLayout):
    pass

class QueryForm(form.Form):
    form_buttons = form.Button(value=_('Search'),
                               _class="btn btn-primary btn-flat btn-xs search",
                               type='submit')
    layout_class = NewQueryLayout
    form_method = 'GET'
