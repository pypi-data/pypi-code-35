# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tab(Component):
    """A Tab component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- style (dict; optional): Defines CSS styles which will override styles previously set. The styles
set here apply to the content of the Tab
- tab_style (dict; optional): Defines CSS styles which will override styles previously set. The styles
set here apply to the NavItem in the tab.
- label_style (dict; optional): Defines CSS styles which will override styles previously set. The styles
set here apply to the NavLink in the tab.
- className (string; optional): Often used with CSS to style elements with common properties.
- key (string; optional): A unique identifier for the component, used to improve
performance by React.js while rendering components
See https://reactjs.org/docs/lists-and-keys.html for more info
- label (string; optional): The tab's label, displayed in the tab itself.
- tab_id (string; optional): Optional identifier for tab used for determining which tab is visible
if not specified, and Tab is being used inside Tabs component, the tabId
will be set to "tab-i" where i is (zero indexed) position of tab in list
tabs pased to Tabs component."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, tab_style=Component.UNDEFINED, label_style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, label=Component.UNDEFINED, tab_id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'style', 'tab_style', 'label_style', 'className', 'key', 'label', 'tab_id']
        self._type = 'Tab'
        self._namespace = 'dash_bootstrap_components/_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'style', 'tab_style', 'label_style', 'className', 'key', 'label', 'tab_id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tab, self).__init__(children=children, **args)
