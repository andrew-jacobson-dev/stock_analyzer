from django.conf import settings
from django.shortcuts import render
from stock_summary.models import StockEOD
from stock_analysis.models import ChartInterval
from datetime import datetime, timedelta
from stock_analysis.forms import LineChartForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def analyzer_index(request):

    # Create form for line chart
    line_chart_form = LineChartForm()

    # Fields for line chart
    labels = []

    line_1_data = []
    line_2_data = []
    line_3_data = []
    line_4_data = []
    line_5_data = []
    line_6_data = []
    line_7_data = []

    # Set default for display values
    line_1_data_hidden = 'true'
    line_2_data_hidden = 'true'
    line_3_data_hidden = 'true'
    line_4_data_hidden = 'true'
    line_5_data_hidden = 'true'
    line_6_data_hidden = 'true'
    line_7_data_hidden = 'true'

    date_ranges = ''
    selected_date_range = ''

    chosen_stock_name = ''

    line_chart_chart_type = ''
    line_chart_y_axis_start_at_zero = ''

    # Get the most recent date of the data
    most_recent_close_date = StockEOD.objects.latest('d_process')
    most_recent_close_date = most_recent_close_date.d_process

    if request.method == 'POST':

        line_chart_form = LineChartForm(request.POST)

        if line_chart_form.is_valid():

            # Determine the selected stock
            chosen_stock_name = str(line_chart_form.cleaned_data['stock'])
            start_position = chosen_stock_name.rfind('[')
            start_position += 1
            end_position = chosen_stock_name.rfind(']')
            chosen_stock_symbol = chosen_stock_name[start_position:end_position]

            # Get the list of possible date ranges
            date_ranges = ChartInterval.objects.filter(i_active=True).order_by('n_page_order')

            # Get the first date range to use as the default
            # chosen_date_range = date_ranges.first()
            # selected_date_range = chosen_date_range.t_short_name
            # chosen_date_range = chosen_date_range.q_days

            if 'date_range' in request.POST:
                selected_date_range = request.POST['date_range']
                selected_date_range_days = ChartInterval.objects.get(t_short_name=selected_date_range)
                selected_date_range_days = selected_date_range_days.q_days
            else:
                selected_date_range = date_ranges.first().t_short_name
                # selected_date_range = selected_date_range.t_short_name
                selected_date_range_days = date_ranges.first().q_days

            # Calculate the date range to use in the StockEOD object lookup
            date_range = datetime.now().date() - timedelta(days=selected_date_range_days)

            # Fetch Stock data based on selections
            stock_data = StockEOD.objects.filter(stock__n_symbol=chosen_stock_symbol, d_process__gte=date_range).select_related('stock').order_by('d_process')

            # Populate data for line chart
            for stock_data in stock_data:
                labels.append(str(stock_data.d_process))
                line_1_data.append(str(stock_data.a_open))
                line_2_data.append(str(stock_data.a_close))
                line_3_data.append(str(stock_data.a_open_close_delta))
                line_4_data.append(str(stock_data.a_low))
                line_5_data.append(str(stock_data.a_high))
                line_6_data.append(str(stock_data.a_low_high_delta))
                line_7_data.append(str(stock_data.a_volume))

            # Get any selected display values
            chart_values = line_chart_form.cleaned_data['chart_values']

            if 'line_1' in chart_values:
                line_1_data_hidden = 'false'
            else:
                line_1_data_hidden = 'true'

            if 'line_2' in chart_values:
                line_2_data_hidden = 'false'
            else:
                line_2_data_hidden = 'true'

            if 'line_3' in chart_values:
                line_3_data_hidden = 'false'
            else:
                line_3_data_hidden = 'true'

            if 'line_4' in chart_values:
                line_4_data_hidden = 'false'
            else:
                line_4_data_hidden = 'true'

            if 'line_5' in chart_values:
                line_5_data_hidden = 'false'
            else:
                line_5_data_hidden = 'true'

            if 'line_6' in chart_values:
                line_6_data_hidden = 'false'
            else:
                line_6_data_hidden = 'true'

            if 'line_7' in chart_values:
                line_7_data_hidden = 'false'
            else:
                line_7_data_hidden = 'true'

            # Get any line chart options selected
            line_chart_chart_type = line_chart_form.cleaned_data['chart_type']

            # Convert to lowercase string for the JS
            line_chart_y_axis_start_at_zero = str(line_chart_form.cleaned_data['y_axis_start_at_zero']).lower()

    else:

        # Fetch default Stock data for line chart
        default_stock = line_chart_form.get_default_stock()
        chosen_stock_name = default_stock
        default_stock_symbol = default_stock.n_symbol

        # Get list of active date ranges for buttons
        date_ranges = ChartInterval.objects.filter(i_active=True).order_by('n_page_order')

        # Get the first date range to use as the default
        first_date_range = date_ranges.first()
        date_range = datetime.now().date() - timedelta(days=first_date_range.q_days)

        # Now assign the selected date range
        selected_date_range = first_date_range.t_short_name

        # Fetch Stock data for default
        stock_data = StockEOD.objects.filter(stock__n_symbol=default_stock_symbol, d_process__gte=date_range).select_related('stock').order_by('d_process')

        # Populate data for line chart
        for stock_data in stock_data:
            labels.append(str(stock_data.d_process))
            line_1_data.append(str(stock_data.a_open))
            line_2_data.append(str(stock_data.a_close))
            line_3_data.append(str(stock_data.a_open_close_delta))
            line_4_data.append(str(stock_data.a_low))
            line_5_data.append(str(stock_data.a_high))
            line_6_data.append(str(stock_data.a_low_high_delta))
            line_7_data.append(str(stock_data.a_volume))

        # Set default for display values
        line_1_data_hidden = 'true'
        line_2_data_hidden = 'false'
        line_3_data_hidden = 'true'
        line_4_data_hidden = 'true'
        line_5_data_hidden = 'true'
        line_6_data_hidden = 'true'
        line_7_data_hidden = 'true'

        # The default for the "chart type" option is set in the form class
        line_chart_chart_type = line_chart_form.get_intial_chart_type()

        # The default for the "start y-axis at 0" option is set in the form class
        line_chart_y_axis_start_at_zero = line_chart_form.get_initial_y_axis_start_at_zero()

#   end if

    table_data = zip(labels, line_1_data, line_2_data, line_3_data)

    context = {
        'line_chart_form': line_chart_form,
        'table_data': table_data,
        'labels': labels,
        'line_1_data': line_1_data,
        'line_1_data_hidden': line_1_data_hidden,
        'line_2_data': line_2_data,
        'line_2_data_hidden': line_2_data_hidden,
        'line_3_data': line_3_data,
        'line_3_data_hidden': line_3_data_hidden,
        'line_4_data': line_4_data,
        'line_4_data_hidden': line_4_data_hidden,
        'line_5_data': line_5_data,
        'line_5_data_hidden': line_5_data_hidden,
        'line_6_data': line_6_data,
        'line_6_data_hidden': line_6_data_hidden,
        'line_7_data': line_7_data,
        'line_7_data_hidden': line_7_data_hidden,
        'date_ranges': date_ranges,
        'selected_date_range': selected_date_range,
        'most_recent_close_date': most_recent_close_date,
        'chosen_stock_name': chosen_stock_name,
        'line_chart_chart_type': line_chart_chart_type,
        'line_chart_y_axis_start_at_zero': line_chart_y_axis_start_at_zero,
    }

    return render(request, 'analyzer.html', context)
