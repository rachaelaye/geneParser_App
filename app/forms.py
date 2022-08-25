from django import forms


class GeneInputForm(forms.Form):
    input_textarea = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 150}))
