from django import forms

class SearchForm(forms.Form):
    #sender = forms.CharField(label='Sender', max_length=100, required=False)
    #receiver = forms.CharField(label='Receiver', max_length=100, required=False)
    client = forms.CharField(label='Client code', max_length=100, required=False)
    text = forms.CharField(label='Search text', max_length=100, required=False)
