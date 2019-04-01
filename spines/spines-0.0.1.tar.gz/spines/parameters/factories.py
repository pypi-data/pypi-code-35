# -*- coding: utf-8 -*-
"""
Parameter factory functions
"""
#
#   Imports
#
from .base import ParameterMixin


#
#   Factory functions
#

def bound_mixin(name, checker, cls_name=None):
    """Creates a new mixin class for bounded parameters

    This factory function makes creating bound mixins very simple, you only
    need to provide the `name` for the attribute on the resulting class for
    this particular boundary condition, and provide a callable `checker`
    to perform the validation.  The checker call needs to look like this:

    .. code-block: python

        def checker(value, boundary):
            ...

    The call should return True when the value is within the boundary and False
    when it's not.  The `checker` doesn't necessarily have to be a function,
    it just needs to be callable.

    Parameters
    ----------
    name : str
        Name of the property holding the bound's value.
    checker : callable
        Callable object/function to assess the boundary condition.
    cls_name : str, optional
        Name for the newly created class type (defaults to `name` +
        'BoundMixin').

    Returns
    -------
    ParameterMixin
        New parameter mixin class for the bound specified.

    Raises
    ------
    ValueError
        If the given `checker` is not callable.

    """
    if not callable(checker):
        raise ValueError("The checker must be callable")
    if not cls_name:
        cls_name = '%sBoundMixin' % name.replace(' ', '')
        cls_name = cls_name[0].upper() + cls_name[1:]

    prop_name = name.lower().replace(' ', '_')
    var_name = '_%s' % prop_name

    def _w_property_get(self):
        return getattr(self, var_name)
    _w_property_get.func = '_get_%s' % prop_name

    def _w_property_set(self, value):
        setattr(self, var_name, value)
    _w_property_set.func = '_set_%s' % prop_name

    w_property = property(
        _w_property_get, _w_property_set, None, "The %s bound" % name
    )

    class _NewBoundMixin(ParameterMixin):

        def __init__(self, *args, **kwargs):
            setattr(self, var_name, None)
            prop_val = kwargs.pop(prop_name, None)

            super(_NewBoundMixin, self).__init__(*args, **kwargs)

            if prop_val:
                setattr(self, prop_name, prop_val)

        def _check_helper(self, value, raise_exceptions=True) -> bool:
            ret = super(_NewBoundMixin, self)._check_helper(
                value, raise_exceptions=raise_exceptions
            )
            return ret and checker(value, getattr(self, var_name))

        def _disp_props(self):
            ret = super(_NewBoundMixin, self)._disp_props()
            bnd = getattr(self, prop_name, None)
            if bnd:
                ret.append('%s=%s' % (prop_name, bnd))
            return ret

    return type(cls_name, (_NewBoundMixin,), {prop_name: w_property})
