
import copy
import datetime
import warnings
from collections import defaultdict
from itertools import chain

from django.forms import widgets
from django.forms.widgets import Select

from django.forms.utils import to_current_timezone
from django.templatetags.static import static
from django.utils import datetime_safe, formats
from django.utils.datastructures import OrderedSet
from django import forms
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.html import format_html, html_safe
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.topological_sort import (
    CyclicDependencyError, stable_topological_sort,
)
from django.utils.translation import gettext_lazy as _


class SecurityQuestionWidget(widgets.MultiWidget):
    """
    A widget that splits graduation date as year and month.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """

    template_name = 'widgets/security_question.html'

    def __init__(self, attrs=None, dt=None, mode=0):
        # bits of python to create days, months, years
        # example below, the rest snipped for neatness.
        year_digits = [2003, 2004, 2005]
        years = [(year, year) for year in year_digits]

        _widgets = (
            widgets.Select(attrs=attrs, choices=years), 
            widgets.PasswordInput(attrs=attrs),
            widgets.PasswordInput(attrs=attrs),
        )

        super().__init__(_widgets, attrs)

    # def format_value(self, value):
    #     """
    #     Return a value as it should appear when rendered in a template.
    #     """
    #     print(value)
    #     return value
    #     if value == '' or value is None:
    #         return None
    #     if self.is_localized:
    #         return formats.localize_input(value)
    #     return str(value)

    # def value_from_datadict(self, data, files, name):
    #     question = data.get("%s_0" % name)
    #     answer = data.get('%s_1' % name)
    #     confirm_answer = data.get('%s_2' % name)

    #     return 'test'
    #     return [question, answer, confirm_answer]
        
        # y = data.get(self.year_field % name)
        # m = data.get(self.month_field % name)
        # d = data.get(self.day_field % name)
        # if y == m == d == '':
        #     return None
        # if y is not None and m is not None and d is not None:
        #     if settings.USE_L10N:
        #         input_format = get_format('DATE_INPUT_FORMATS')[0]
        #         try:
        #             date_value = datetime.date(int(y), int(m), int(d))
        #         except ValueError:
        #             pass
        #         else:
        #             date_value = datetime_safe.new_date(date_value)
        #             return date_value.strftime(input_format)
        #     # Return pseudo-ISO dates with zeros for any unselected values,
        #     # e.g. '2017-0-23'.
        #     return '%s-%s-%s' % (y or 0, m or 0, d or 0)
        # return data.get(name)
        
    def decompress(self, value):
        if value:
            print(value)
            return ['123']
        return [None, None, None]

class SecurityQuestionField(forms.CharField):
    widget = SecurityQuestionWidget
