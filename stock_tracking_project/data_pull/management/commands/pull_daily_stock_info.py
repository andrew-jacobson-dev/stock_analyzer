from django.core.management.base import BaseCommand, CommandError
from stock_summary.models import Stock, StockEOD, StockRecommendation
from datetime import datetime, timedelta
import yfinance as yf

class Command(BaseCommand):

    help = 'Fetches the daily stock data using the yfinance API'

    def add_arguments(self, parser):

        parser.add_argument(
            '-stocks',
            '--ticker_symbol',
            type=str,
            nargs=1,
            help="Enter the ticker symbol for the stock you'd like to pull the data for."
        )

    def handle(self, *args, **kwargs):

        # If a stock is specified, only pull data for that stock
        if kwargs['ticker_symbol']:
            # Get value from command args
            ticker_symbol = kwargs['ticker_symbol'][0]
            ticker_symbol = ticker_symbol.upper()
            # Look up Stock object
            stocks = Stock.objects.filter(n_symbol=ticker_symbol)
        else:
            # If no argument specified, get all Stock objects
            stocks = Stock.objects.all()

        # Get date to use for d_process
        data_date = datetime.now().date() - timedelta(1)

        # Error counter
        error_counter = 0

        for stock in stocks:

            if error_counter < 5:

                try:
                    # Fetch stock information using yfinance Ticker
                    yfinance_stock = yf.Ticker(stock.n_symbol)

                    insert_StockEOD(stock, data_date, yfinance_stock)
                    insert_StockRecommendation(stock, yfinance_stock)

                except Exception as e:
                    error_counter += 1
                    self.stdout.write(self.style.ERROR('Could not pull yfinance data for %s: %s' % (stock.n_symbol, e)))


def insert_StockEOD(Stock, data_date, yfinance_Ticker):

    # Create StockEOD object for insert
    stockEOD_stock = Stock
    stockEOD_d_process = data_date
    stockEOD_a_open = yfinance_Ticker.info['open']
    stockEOD_a_close = yfinance_Ticker.history(period="1d")['Close'][0]
    stockEOD_a_open_close_delta = stockEOD_a_close - stockEOD_a_open
    stockEOD_a_previous_close = yfinance_Ticker.info['previousClose']
    stockEOD_a_close_delta = stockEOD_a_close - stockEOD_a_previous_close
    stockEOD_a_low = yfinance_Ticker.info['dayLow']
    stockEOD_a_high = yfinance_Ticker.info['dayHigh']
    stockEOD_a_low_high_delta = stockEOD_a_high - stockEOD_a_low
    stockEOD_a_fifty_two_week_high = yfinance_Ticker.info['fiftyTwoWeekHigh']
    stockEOD_a_fifty_two_week_low = yfinance_Ticker.info['fiftyTwoWeekLow']
    stockEOD_a_fifty_two_week_delta = stockEOD_a_fifty_two_week_high - stockEOD_a_fifty_two_week_low
    stockEOD_a_ask = yfinance_Ticker.info['ask']
    stockEOD_q_ask_size = yfinance_Ticker.info['askSize']
    stockEOD_a_bid = yfinance_Ticker.info['bid']
    stockEOD_q_bid_size = yfinance_Ticker.info['bidSize']
    stockEOD_a_two_hundred_day_avg = yfinance_Ticker.info['twoHundredDayAverage']
    stockEOD_a_fifty_day_avg = yfinance_Ticker.info['fiftyDayAverage']
    stockEOD_a_volume = yfinance_Ticker.info['volume']
    stockEOD_a_avg_volume = yfinance_Ticker.info['averageVolume']
    stockEOD_a_ten_day_volume_avg = yfinance_Ticker.info['averageVolume10days']
    stockEOD_a_payout_ratio = yfinance_Ticker.info['payoutRatio']
    stockEOD_a_beta = yfinance_Ticker.info['beta']
    stockEOD_a_market_cap = yfinance_Ticker.info['marketCap']
    stockEOD_a_forward_pe = yfinance_Ticker.info['forwardPE']
    stockEOD_a_forward_eps = yfinance_Ticker.info['forwardEps']
    stockEOD_a_trailing_eps = yfinance_Ticker.info['trailingEps']

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

    # Try saving/inserting the object
    try:
        # stockEOD_insert.save()
        print('saving EOD', Stock.n_symbol)
    except Exception as e:
        print('Error inserting data for', Stock.n_symbol, '-', e)
    finally:
        return


def insert_StockRecommendation(Stock, yfinance_Ticker):

    # Create StockRecommendation object for insert
    stockRecommendation_stock = Stock
    recommendations = yfinance_Ticker.recommendations

    for index, row in recommendations.iterrows():

        stockRecommendation_s_recommendation = str(index.to_pydatetime())
        stockRecommendation_t_firm = row['Firm']
        stockRecommendation_t_to_grade = row['To Grade']
        stockRecommendation_t_from_grade = row['From Grade']

        stockRecommendation_insert = StockRecommendation(
            stock=stockRecommendation_stock,
            s_recommendation=stockRecommendation_s_recommendation,
            t_firm=stockRecommendation_t_firm,
            t_to_grade=stockRecommendation_t_to_grade,
            t_from_grade=stockRecommendation_t_from_grade,
        )

        # print(stockRecommendation_insert.s_recommendation)
