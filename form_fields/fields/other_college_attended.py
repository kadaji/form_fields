
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


class OtherCollegeAttendedWidget(widgets.MultiWidget):
    """
    A widget that asks security questions and 2 verification answers.
    """

    template_name = 'widgets/other_college_attended.html'

    def __init__(self, attrs=None, questions=[], mode=0):
        _widgets = (
            widgets.Select(attrs=attrs, choices=[
                ('', 'Select'),
                (1424, 'Allen County Community College'),
                (1386, 'Baker University'),
                (1411, 'Barclay College'),
                (1387, 'Barton County Comm College'),
                (1444, 'Benedictine College'),
                (1388, 'Bethany College'),
                (1390, 'Bethel College'),
                (4757, 'Brown Mackie Coll-Salina'),
                (1406, 'Butler Community College'),
                (1394, 'Central Christian College-KS'),
                (1401, 'Cloud County Community College'),
                (1398, 'Coffeyville Community College'),
                (1399, 'Colby Community College'),
                (1384, 'Cowley County Comm College'),
                (1402, 'Dodge City Comm Coll-Tech Ctr'),
                (1404, 'Donnelly College'),
                (1430, 'Emporia State University'),
                (45, 'Flinthills Technical College'),
                (1408, 'Fort Hays State University'),
                (1410, 'Fort Scott Community College'),
                (1412, 'Friends University'),
                (1414, 'Garden City Community College'),
                (749, 'Haskell Indian Jr College'),
                (1415, 'Haskell Indian Nations Univ'),
                (1416, 'Hesston College'),
                (1418, 'Highland Community College'),
                (1420, 'Hutchinson Community College'),
                (1422, 'Independence Community College'),
                (1425, 'Johnson County Comm College'),
                (1426, 'Kansas City Kansas Comm Coll'),
                (1428, 'Kansas State University'),
                (1434, 'Kansas Wesleyan University'),
                (782, 'KS School of Hair Styling'),
                (1453, 'K-State Salina Coll of Tech'),
                (1448, 'Labette Community College'),
                (1447, 'Manhattan Area Tech College'),
                (1436, 'Manhattan Christian College'),
                (1440, 'McPherson College'),
                (1445, 'MidAmerica Nazarene College'),
                (1396, 'Neosho County Comm College'),
                (1452, 'Newman University'),
                (1451, 'North Central KS Tech College'),
                (1437, 'Northeast Kansas Tech College'),
                (5574, 'Northwest Kansas Tech School'),
                (1446, 'Ottawa University'),
                (1449, 'Pittsburg State University'),
                (1450, 'Pratt Community College'),
                (1459, 'Salina Area Tech College'),
                (1439, 'Seward County Comm College'),
                (1461, 'Southwest Kansas Tech School'),
                (1464, 'Southwestern College'),
                (1455, 'St Mary\'s College'),
                (1466, 'Sterling College'),
                (1468, 'Tabor College'),
                (1421, 'Topeka Technical College'),
                (725, 'United Technical Institute'),
                (6063, 'Univ. of Kansas Med. Center'),
                (1470, 'University of Kansas'),
                (1458, 'University of Saint Mary'),
                (296, 'Washburn Institute of Tech'),
                (1474, 'Washburn University'),
                (1472, 'Wichita State University'),
                (173204, 'WSU Tech')
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
