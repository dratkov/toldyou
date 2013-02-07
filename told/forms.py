# -*- coding: utf-8 -*-
import datetime
from models import *

from django import forms

class PostForm(forms.Form):
    text = forms.CharField(max_length = 280, error_messages = {'required': "Не может быть пустым!", 'max_length': "Не более 280 символов!"})
    event_date = forms.DateTimeField( error_messages={}, required=False)

    def clean_event_date(self):
        data = self.cleaned_data['event_date']
        print data
        print datetime.datetime.now()
        if data.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
            raise forms.ValidationError("Должно произойти в будушем!")
        if not data:
            return data