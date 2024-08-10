from django import forms 
from .models import Upload
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    captcha = CaptchaField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Upload 
        fields = ("post_type", "meta_file", "body_file", )