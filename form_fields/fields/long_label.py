from django import forms
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe

class LongLabelWidget(widgets.Input):
    template_name = 'widgets/long_label.html'

    def __init__(self, attrs=None):
        default_attrs = {}

        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

class LongLabelField(forms.Field):
    widget = LongLabelWidget
