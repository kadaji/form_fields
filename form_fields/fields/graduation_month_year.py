
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
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.html import format_html, html_safe
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.topological_sort import (
    CyclicDependencyError, stable_topological_sort,
)
from django.utils.translation import gettext_lazy as _


class GraduationMonthYearWidget(widgets.SelectDateWidget):
    """
    A widget that splits graduation date as year and month.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """

    # none_value = ('', '---')
    # month_field = '%s_month'
    # day_field = '%s_day'
    # year_field = '%s_year'
    # template_name = 'django/forms/widgets/select_date.html'
    # input_type = 'select'
    # select_widget = Select
    date_re = _lazy_re_compile(r'(\d{4}|0)-(\d\d?)$')

    default_date = 1

    def __init__(self, attrs=None, years=None, months=None, empty_label=None):

        # Optional list or tuple of years to use in the "year" select box.
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 4)

        super().__init__(attrs, years, months, empty_label)

    def format_value(self, value):
        """
        Return a dict containing the year, month, and day of the current value.
        Use dict instead of a datetime to allow invalid dates such as February
        31 to display correctly.
        """
        year, month = None, None
        if isinstance(value, (datetime.date, datetime.datetime)):
            year, month, day = value.year, value.month, value.day
        elif isinstance(value, str):

            match = self.date_re.match(value)
            if match:
                # Convert any zeros in the date to empty strings to match the
                # empty option value.
                year, month = [int(val) or '' for val in match.groups()]
            else:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    d = datetime.datetime.strptime(value, input_format)
                except ValueError:
                    pass
                else:
                    year, month = d.year, d.month
        return {'year': year, 'month': month, 'day': self.default_date}

    @staticmethod
    def _parse_date_fmt():
        fmt = "N Y"

        escaped = False
        for char in fmt:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char in 'Yy':
                yield 'year'
            elif char in 'bEFMmNn':
                yield 'month'
            elif char in 'dj':
                yield 'day'

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)

        d = data.get(self.day_field % name)
        if y == m == '':
            return None

        if y is not None and m is not None:
            input_format = get_format('DATE_INPUT_FORMATS')[0]
            # print(input_format)

            try:
                date_value = datetime.date(int(y), int(m), self.default_date)
            except ValueError:
                # Return pseudo-ISO dates with zeros for any unselected values,
                # e.g. '2017-0-23'.
                return '%s-%s-%s' % (y or 0, m or 0, d or 0)
            date_value = datetime_safe.new_date(date_value)
            return date_value.strftime(input_format)
        return data.get(name)
