
import copy
import datetime
import warnings
from collections import defaultdict
from itertools import chain

from django.forms import widgets
from django.forms.widgets import Select

from django.forms.utils import to_current_timezone
from django.templatetags.static import static
from django.utils.datastructures import OrderedSet
from django import forms
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.html import format_html, html_safe
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class OtherCollegeAttendedWidget(widgets.MultiWidget):
    """
    A widget that asks security questions and 2 verification answers.
    """

    template_name = 'widgets/other_college_attended.html'

    def __init__(self, attrs=None, questions=[], mode=0):
        _widgets = (
            widgets.Select(attrs=attrs, choices=[
                
                ('', 'Select'),
                ('6305', 'Allen County Community College'),
                ('6031', 'Baker University'),
                ('6228', 'Barclay College'),
                ('0784', 'Barton County Comm College'),
                ('6056', 'Benedictine College'),
                ('6034', 'Bethany College'),
                ('6037', 'Bethel College'),
                ('1194', 'Bethel House Training Inst-no'),
                ('3366', 'Brown Mackie Coll-Salina'),
                ('6191', 'Butler Community College'),
                ('6088', 'Central Christian College-KS'),
                ('6137', 'Cloud County Community College'),
                ('6102', 'Coffeyville Community College'),
                ('6129', 'Colby Community College'),
                ('6008', 'Cowley County Comm College'),
                ('6166', 'Dodge City Comm Coll-Tech Ctr'),
                ('6167', 'Donnelly College'),
                ('6335', 'Emporia State University'),
                ('6232', 'Flinthills Technical College'),
                ('6218', 'Fort Hays State University'),
                ('6219', 'Fort Scott Community College'),
                ('6224', 'Friends University'),
                ('6246', 'Garden City Community College'),
                ('0919', 'Haskell Indian Nations Univ'),
                ('6274', 'Hesston College'),
                ('6276', 'Highland Community College'),
                ('6281', 'Hutchinson Community College'),
                ('6304', 'Independence Community College'),
                ('6325', 'Johnson County Comm College'),
                ('6333', 'Kansas City Kansas Comm Coll'),
                ('6334', 'Kansas State University'),
                ('6337', 'Kansas Wesleyan University'),
                ('1172', 'K-State Salina Coll of Tech'),
                ('6576', 'Labette Community College'),
                ('6392', 'Manhattan Christian College'),
                ('6404', 'McPherson College'),
                ('6437', 'MidAmerica Nazarene College'),
                ('6093', 'Neosho County Comm College'),
                ('6615', 'Newman University'),
                ('2616', 'North Central KS Tech College'),
                ('6547', 'Ottawa University'),
                ('6336', 'Pittsburg State University'),
                ('6581', 'Pratt Community College'),
                ('0321', 'Remington Coll-Wichita no cred'),
                ('0286', 'Seward County Comm College'),
                ('6670', 'Southwestern College'),
                ('6690', 'St Mary\'s College'),
                ('6684', 'Sterling College'),
                ('6815', 'Tabor College'),
                ('0414', 'Univ. of Kansas Med. Center'),
                ('6871', 'University of Kansas'),
                ('6630', 'University of Saint Mary'),
                ('6928', 'Washburn University'),
                ('6884', 'Wichita State University')
            ]),
            
            widgets.Select(attrs=attrs, choices=[
                ('', 'Select'),
                ('january', 'January'),
                ('february', 'February'),
                ('march', 'March'),
                ('april', 'April'),
                ('may', 'May'),
                ('june', 'June'),
                ('july', 'July'),
                ('august', 'August'),
                ('september', 'September'),
                ('october', 'October'),
                ('november', 'November'),
                ('december', 'December'),
            ]),
            widgets.TextInput(attrs=attrs),
            
            widgets.Select(attrs=attrs, choices=[
                ('', 'Select'),
                ('january', 'January'),
                ('february', 'February'),
                ('march', 'March'),
                ('april', 'April'),
                ('may', 'May'),
                ('june', 'June'),
                ('july', 'July'),
                ('august', 'August'),
                ('september', 'September'),
                ('october', 'October'),
                ('november', 'November'),
                ('december', 'December'),
            ]),
            widgets.TextInput(attrs=attrs),

            widgets.Select(attrs=attrs, choices=[
                ('', 'Select'),
                ('yes', 'Yes'),
                ('no', 'No'),
            ]),
        )

        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return ['1', '2', '3']
    
        return [None, None, None]

class OtherCollegeAttendedField(forms.CharField):
    widget = OtherCollegeAttendedWidget
