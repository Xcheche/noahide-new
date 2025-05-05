# subscribers/forms.py
from django import forms

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
