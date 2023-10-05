# forms.py
from django import forms


class WebURLForm(forms.Form):
    target_url = forms.URLField(max_length=200,
                                label='Target URL', help_text="Please enter url of a website for analyzing.",widget=forms.TextInput(attrs={'placeholder': 'https://example.com'}))
