from django import forms 

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)