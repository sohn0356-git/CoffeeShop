from django import forms
from cfboard.models import Cfboard

from django_summernote.fields import SummernoteTextFormField
from django_summernote.widgets import SummernoteWidget

class PostboardForm(forms.Form):
    contents = SummernoteTextFormField()
    class Meta:
        model = Cfboard
        fields = ['title','contents','catename','disclosure']
        widgets = {
            'contents' : SummernoteWidget()
        }