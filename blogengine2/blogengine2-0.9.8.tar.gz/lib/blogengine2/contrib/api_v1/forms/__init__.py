#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .widgets import *

__all__ = ['DynamicField', 'EntryForm', 'DeleteForm']

class DynamicField(forms.ChoiceField):
    '''ChoiceField subclass with builtin autocomplete widget functionality
    
    By default, use the ``choices`` argument as default iterable of values.
    '''

    def __init__(self, *args, **kwargs):
        # initialize autocomplete widget
        kwargs['widget'] = DynamicTextInput(kwargs['choices'])
        super(DynamicField, self).__init__(*args, **kwargs)

class CategoryForm(forms.Form):
    name = forms.CharField(required=True, label="Name")
    slug = forms.CharField(required=True)

class EntryForm(forms.Form):
    """Basic article entry form.""" 
    def __init__(self, db, data=None):
        self.db = db
        #self.required = kwargs.get('category_required', True)
        self.category_choices = [("%s" % item.name, item.name) for item in \
            db.Category.find()
        ]
        if self.category_choices:
            self.declared_fields['category'] = forms.ChoiceField(
                choices=self.category_choices, \
                required=True, 
                label='Category')
        super(EntryForm, self).__init__(data=data)

    content = forms.CharField(label='Text (HTML)', \
        widget=forms.Textarea(attrs={'rows':15, 'cols':35}),
        required=True, help_text='You can use markdown syntax here')

class DeleteForm(forms.Form):
    confirm_unpublish = forms.BooleanField(label='Unpublish this entry?', required=False, initial=True)
    confirm_delete = forms.BooleanField(label='Delete this entry permanently?', required=True, initial=False)

