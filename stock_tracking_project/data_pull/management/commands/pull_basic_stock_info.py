from django.core.management.base import BaseCommand, CommandError
from stock_summary.models import Stock
import yfinance as yf

class Command(BaseCommand):

    help = 'Fetches the basic stock data using the yfinance API'

    def add_arguments(self, parser):

        parser.add_argument(
            'ticker_symbol',
            nargs='+',
            type=str,
            help="Enter the ticker symbol(s) for the stock you'd like to pull the data for, separated by spaces."
        )

    def handle(self, *args, **kwargs):

        for symbol in kwargs['ticker_symbol']:

            try:
                # Fetch stock information using yfinance Ticker
                symbol = symbol.upper()
                yfinance_stock = yf.Ticker(symbol)

                # Create Stock object for insert
                stock_n_symbol = yfinance_stock.info['symbol']
                stock_c_exchange = yfinance_stock.info['exchange']
                stock_t_sector = yfinance_stock.info['sector']
                stock_t_industry = yfinance_stock.info['industry']
                stock_t_short_name = yfinance_stock.info['shortName']
                stock_t_long_name = yfinance_stock.info['longName']
                stock_t_website_url = yfinance_stock.info['website']
                stock_t_logo_url = yfinance_stock.info['logo_url']
                # The field may or may not be there, so need a try/except
                try:
                    stock_a_full_time_employees = yfinance_stock.info['fullTimeEmployees']
                except:
                    stock_a_full_time_employees = 0
                # The field may or may not be there, so need a try/except
                try:
                    stock_c_state = yfinance_stock.info['state']
                except:
                    stock_c_state = ''

                stock_insert = Stock(
                    n_symbol=stock_n_symbol,
                    c_exchange=stock_c_exchange,
                    t_sector=stock_t_sector,
                    t_industry=stock_t_industry,
                    t_short_name=stock_t_short_name,
                    t_long_name=stock_t_long_name,
                    t_website_url=stock_t_website_url,
                    t_logo_url=stock_t_logo_url,
                    a_full_time_employees=stock_a_full_time_employees,
                    c_state=stock_c_state
                )

                # Try saving/inserting the object. If unsuccessful, try updating it.
                try:
                    stock_insert.save()
                except:
                    Stock.objects.filter(n_symbol=stock_n_symbol).update(
                        c_exchange=stock_c_exchange,
                        t_sector=stock_t_sector,
                        t_industry=stock_t_industry,
                        t_short_name=stock_t_short_name,
                        t_long_name=stock_t_long_name,
                        t_website_url=stock_t_website_url,
                        t_logo_url=stock_t_logo_url,
                        a_full_time_employees=stock_a_full_time_employees,
                        c_state=stock_c_state
                    )

            except Exception as e:
                self.stdout.write(self.style.ERROR('Could not pull yfinance data for %s: %s' % (symbol, e)))
