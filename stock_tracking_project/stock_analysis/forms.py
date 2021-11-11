from django import forms
from stock_summary.models import Stock
from django.db.models import Value
from django.db.models.functions import Concat


class LineChartForm(forms.Form):
    # TODO: only show stocks that the user has added
    # Stock selection
    default_stock = Stock.objects.filter().order_by('t_short_name').first()

    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all().order_by('t_short_name'),
        initial=default_stock,
        label="select a stock:",
        widget=forms.Select(attrs={
            "class": "form-control",
            "onchange": "this.form.submit()"
        })
    )

    def get_default_stock(self):

        return self.default_stock

    # Stock type selection
    # default_stock_type = 'all'
    # stock_type_choices = [('all', 'all'), ('watching', 'watching'), ('owned', 'owned')]
    #
    # stock_type = forms.ChoiceField(
    #     initial='all',
    #     required=True,
    #     choices=stock_type_choices,
    #     widget=forms.RadioSelect(attrs={
    #         "class": "stock-type-radio-list"
    #     })
    # )

    # Chart values
    default_chart_value = 'line_2'
    chart_value_choices = [('line_1', 'open'), ('line_2', 'close'), ('line_3', 'open/close diff'),
                           ('line_4', 'low'), ('line_5', 'high'), ('line_6', 'low/high diff'),
                           ('line_7', 'volume')]

    chart_values = forms.MultipleChoiceField(
        initial=default_chart_value,
        required=True,
        label="display values:",
        choices=chart_value_choices,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control"
        })
    )

    def get_chart_values_choices(self):

        return self.chart_value_choices

    def get_chart_values_choices_dict(self):

        temp_dict = {}
        chart_value_choices = self.chart_value_choices

        for value in chart_value_choices:
            # Get the first value in the list (e.g. line_1)
            temp_value = value[0]
            # Set the value of that key to empty
            temp_dict[temp_value] = ''

        return temp_dict

    # Chart type
    default_chart_type = 'line'
    chart_choices = [('line', 'line'), ('bar', 'bar')]

    chart_type = forms.ChoiceField(
        initial=default_chart_type,
        label="chart type:",
        choices=chart_choices,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    def get_intial_chart_type(self):

        return self.default_chart_type

    # Start Y axis at zero
    default_y_axis_start_at_zero = False

    y_axis_start_at_zero = forms.BooleanField(
        initial=default_y_axis_start_at_zero,
        required=False,
        label="start y-axis at 0:"
    )

    def get_initial_y_axis_start_at_zero(self):

        return str(self.default_y_axis_start_at_zero).lower()

    #
