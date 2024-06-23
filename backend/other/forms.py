from django import forms 

class MdHtmlForm(forms.Form):
    markdown = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Paste your markdown here.."
        })
    )