from django import forms
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe

class SignatureWidget(widgets.TextInput):
    template_name = 'widgets/signature.html'

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/signature_pad@2.3.2/dist/signature_pad.min.js',
        )

class SignatureField(forms.CharField):
    widget = SignatureWidget
