
import copy
import datetime
import warnings
from collections import defaultdict
from itertools import chain

from django.forms import widgets
from django.forms.widgets import Select

from django.forms.utils import to_current_timezone
from django.templatetags.static import static
from django.utils import formats
from django.utils.datastructures import OrderedSet
from django import forms
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.html import format_html, html_safe
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class SecurityQuestionWidget(widgets.MultiWidget):
    """
    A widget that asks security questions and 2 verification answers.
    """

    template_name = 'widgets/security_question.html'

    def __init__(self, attrs=None, questions=[], mode=0):
        _widgets = (
            widgets.Select(attrs=attrs, choices=questions), 
            widgets.PasswordInput(attrs=attrs),
            widgets.PasswordInput(attrs=attrs),
        )

        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return ['123']
        return [None, None, None]

class SecurityQuestionField(forms.CharField):
    widget = SecurityQuestionWidget
