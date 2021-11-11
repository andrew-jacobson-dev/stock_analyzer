from django.core.management.base import BaseCommand, CommandError
from stock_summary.models import Stock, StockEOD
from datetime import datetime, timedelta
import yfinance as yf
from pandas._libs.tslibs.timestamps import Timestamp
from django.core.exceptions import ValidationError

class Command(BaseCommand):

    help = 'Fetches historical stock data for newly added stocks for a specified date range using the yfinance API'

    def add_arguments(self, parser):

        parser.add_argument(
            'ticker_symbol',
            nargs=1,
            type=str,
            help="Enter the ticker symbol for the stock you'd like to pull the data for."
        )

    def handle(self, *args, **kwargs):

        ticker_symbol = kwargs['ticker_symbol'][0]
        current_date = str(datetime.now().strftime('%Y-%m-%d'))

        try:
            # Fetch stock information using yfinance Ticker
            yfinance_stock = yf.Ticker(ticker_symbol)
            stock_history = yfinance_stock.history(period="Max")

            # Get Stock object from database
            stock = Stock.objects.get(n_symbol=ticker_symbol)

            # Variables used for calculations
            temp_previous_close = 0

            # Iterate through the historical dataframe
            for index, row in stock_history.iterrows():

                # Create StockEOD object for insert
                stockEOD_stock = stock
                stockEOD_d_process = str(index.to_pydatetime()).split()[0]

                # Close and Previous Close
                stockEOD_a_close = round(row['Close'], 3)
                stockEOD_a_previous_close = temp_previous_close
                temp_previous_close = round(row['Close'], 3)
                stockEOD_a_close_delta = stockEOD_a_close - stockEOD_a_previous_close

                stockEOD_a_open = round(row['Open'], 3)
                stockEOD_a_open_close_delta = stockEOD_a_close - stockEOD_a_open
                stockEOD_a_low = round(row['Low'], 3)
                stockEOD_a_high = round(row['High'], 3)
                stockEOD_a_low_high_delta = stockEOD_a_high - stockEOD_a_low
                stockEOD_a_low_high_delta = round(stockEOD_a_low_high_delta, 3)
                stockEOD_a_fifty_two_week_high = 0
                stockEOD_a_fifty_two_week_low = 0
                stockEOD_a_fifty_two_week_delta = stockEOD_a_fifty_two_week_high - stockEOD_a_fifty_two_week_low
                stockEOD_a_ask = 0
                stockEOD_q_ask_size = 0
                stockEOD_a_bid = 0
                stockEOD_q_bid_size = 0
                stockEOD_a_two_hundred_day_avg = 0
                stockEOD_a_fifty_day_avg = 0
                stockEOD_a_volume = round(row['Volume'])
                stockEOD_a_avg_volume = 0
                stockEOD_a_ten_day_volume_avg = 0
                stockEOD_a_payout_ratio = 0
                stockEOD_a_beta = 0
                stockEOD_a_market_cap = 0
                stockEOD_a_forward_pe = 0
                stockEOD_a_forward_eps = 0
                stockEOD_a_trailing_eps = 0

                # Ignore the intraday numbers
                if stockEOD_d_process != current_date:

                    try:

                        # Create the StockEOD object
                        stockEOD_insert = StockEOD(
                            stock=stockEOD_stock,
                            d_process=stockEOD_d_process,
                            a_open=stockEOD_a_open,
                            a_close=stockEOD_a_close,
                            a_open_close_delta=stockEOD_a_open_close_delta,
                            a_previous_close=stockEOD_a_previous_close,
                            a_close_delta=stockEOD_a_close_delta,
                            a_low=stockEOD_a_low,
                            a_high=stockEOD_a_high,
                            a_low_high_delta=stockEOD_a_low_high_delta,
                            a_fifty_two_week_high=stockEOD_a_fifty_two_week_high,
                            a_fifty_two_week_low=stockEOD_a_fifty_two_week_low,
                            a_fifty_two_week_delta=stockEOD_a_fifty_two_week_delta,
                            a_ask=stockEOD_a_ask,
                            q_ask_size=stockEOD_q_ask_size,
                            a_bid=stockEOD_a_bid,
                            q_bid_size=stockEOD_q_bid_size,
                            a_two_hundred_day_avg=stockEOD_a_two_hundred_day_avg,
                            a_fifty_day_avg=stockEOD_a_fifty_day_avg,
                            a_volume=stockEOD_a_volume,
                            a_avg_volume=stockEOD_a_avg_volume,
                            a_ten_day_volume_avg=stockEOD_a_ten_day_volume_avg,
                            a_payout_ratio=stockEOD_a_payout_ratio,
                            a_beta=stockEOD_a_beta,
                            a_market_cap=stockEOD_a_market_cap,
                            a_forward_pe=stockEOD_a_forward_pe,
                            a_forward_eps=stockEOD_a_forward_eps,
                            a_trailing_eps=stockEOD_a_trailing_eps,
                        )

                        # Try saving/inserting the object. If unsuccessful,
                        try:
                            stockEOD_insert.save()
                        except Exception as e:
                            print(e)
                            self.stdout.write(self.style.ERROR('Error inserting data for %s' % stock.n_symbol))

                    # If there is an error creating the database object
                    except Exception as e:
                        print(e)
        except:
            self.stdout.write(self.style.ERROR('Could not pull yfinance data for %s' % ticker_symbol))
