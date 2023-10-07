# forms.py
from django import forms


class WebURLForm(forms.Form):
    target_url = forms.URLField(max_length=200,
                                label='',
                                help_text="Please enter the address of an English-language website for analysis.",
                                widget=forms.TextInput(attrs={'placeholder': 'https://example.com'}))
