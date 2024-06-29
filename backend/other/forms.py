from django import forms 

class MdHtmlForm(forms.Form):

    markdown = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write or paste your markdown here..",
        }),
        label=''
    )

    def  __init__(self, *args, **kwargs):
        super(MdHtmlForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'parser'