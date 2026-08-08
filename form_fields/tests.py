import datetime

from django.test import SimpleTestCase

from form_fields.fields.graduation_month_year import GraduationMonthYearWidget


class GraduationMonthYearWidgetYearRangeTests(SimpleTestCase):
    """The widget must offer the range it computes.

    ``__init__`` derived a four-year range into ``self.years`` and then called
    ``super().__init__(attrs, years, ...)`` with the *original* ``years``
    argument — ``None`` when the caller passed nothing — so ``SelectDateWidget``
    promptly overwrote ``self.years`` with its stock ten-year range.

    That is not cosmetic. Consumers derive a student's grade level from the
    graduation year, and only four years map to a grade (senior through
    freshman). Offering ten means most selectable years produce a student with
    no derivable grade level, and downstream that makes their registration
    invisible rather than invalid.
    """

    def _expected_default_range(self, today=None):
        today = today or datetime.date.today()
        first = today.year + 1 if today.month >= 5 else today.year
        return list(range(first, first + 4))

    def test_default_range_is_the_four_years_it_computes(self):
        widget = GraduationMonthYearWidget()
        self.assertEqual(list(widget.years), self._expected_default_range())

    def test_default_range_offers_exactly_four_years(self):
        widget = GraduationMonthYearWidget()
        self.assertEqual(len(list(widget.years)), 4)

    def test_explicit_years_are_honoured(self):
        widget = GraduationMonthYearWidget(years=[2027, 2028, 2029, 2030])
        self.assertEqual(list(widget.years), [2027, 2028, 2029, 2030])

    def test_rendered_options_match_the_computed_range(self):
        """Guard the rendering too — self.years is what reaches the template."""
        widget = GraduationMonthYearWidget()
        html = widget.render('graduation_date', None, attrs={'id': 'id_grad'})
        for year in self._expected_default_range():
            self.assertIn(f'value="{year}"', html)
        # A year one past the computed window must not be offered.
        beyond = self._expected_default_range()[-1] + 1
        self.assertNotIn(f'value="{beyond}"', html)
