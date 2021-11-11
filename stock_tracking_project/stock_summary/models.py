from django.db import models


# Create your models here.
class Stock(models.Model):

    n_symbol = models.CharField(max_length=5, unique=True)
    c_exchange = models.CharField(max_length=5)
    t_sector = models.CharField(max_length=50)
    t_industry = models.CharField(max_length=50)
    t_short_name = models.CharField(max_length=50)
    t_long_name = models.CharField(max_length=75)
    t_website_url = models.CharField(max_length=60)
    t_logo_url = models.CharField(max_length=60)
    a_full_time_employees = models.BigIntegerField()
    c_state = models.CharField(max_length=2)
    d_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['t_short_name']

    def __str__(self):
        return self.t_short_name + " [" + self.n_symbol + "]"


class SectorIndustryPerformance(models.Model):

    t_sector = models.CharField(max_length=50)
    t_industry = models.CharField(max_length=50)
    d_evaluated = models.DateField()
    a_forward_eps = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    a_trailing_eps = models.DecimalField(max_digits=10, decimal_places=3, null=True)

class StockRecommendation(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    s_recommendation = models.DateTimeField()
    t_firm = models.CharField(max_length=50)
    t_to_grade = models.CharField(max_length=50)
    t_from_grade = models.CharField(max_length=50)
    t_action = models.CharField(max_length=10)

    class Meta:
        unique_together = ('stock', 's_recommendation', 't_firm', 't_to_grade', 't_from_grade', 't_action')

    def __str__(self):
        return "[" + self.stock.n_symbol + "] " + self.t_firm + ' - ' + str(self.s_recommendation)

class StockEOD(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    d_process = models.DateField()
    s_inserted = models.DateTimeField(auto_now_add=True)
    s_updated = models.DateTimeField(auto_now=True)

    a_open = models.DecimalField(max_digits=10, decimal_places=3)
    a_close = models.DecimalField(max_digits=10, decimal_places=3)
    a_open_close_delta = models.DecimalField(max_digits=10, decimal_places=3)
    a_previous_close = models.DecimalField(max_digits=10, decimal_places=3)
    a_close_delta = models.DecimalField(max_digits=10, decimal_places=3)

    a_low = models.DecimalField(max_digits=10, decimal_places=3)
    a_high = models.DecimalField(max_digits=10, decimal_places=3)
    a_low_high_delta = models.DecimalField(max_digits=10, decimal_places=3)

    a_fifty_two_week_high = models.DecimalField(max_digits=10, decimal_places=3)
    a_fifty_two_week_low = models.DecimalField(max_digits=10, decimal_places=3)
    a_fifty_two_week_delta = models.DecimalField(max_digits=10, decimal_places=3)

    a_ask = models.DecimalField(max_digits=10, decimal_places=3)
    q_ask_size = models.BigIntegerField()
    a_bid = models.DecimalField(max_digits=10, decimal_places=3)
    q_bid_size = models.BigIntegerField()
    a_two_hundred_day_avg = models.DecimalField(max_digits=10, decimal_places=5)
    a_fifty_day_avg = models.DecimalField(max_digits=10, decimal_places=5)
    a_volume = models.BigIntegerField()
    a_avg_volume = models.BigIntegerField()
    a_ten_day_volume_avg = models.BigIntegerField()

    a_payout_ratio = models.IntegerField(null=True)
    a_beta = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    a_market_cap = models.BigIntegerField(null=True)
    a_forward_pe = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    a_forward_eps = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    a_trailing_eps = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    class Meta:
        unique_together = ('stock', 'd_process')
        ordering = ['-d_process', 'stock__n_symbol']

    def __str__(self):
        return str(self.d_process) + " - " + self.stock.t_short_name + " [" + self.stock.n_symbol + "]"


class StockEODProfile(models.Model):

    stockeod = models.ForeignKey(StockEOD, on_delete=models.CASCADE)
    d_evaluation = models.DateField()
    t_status = models.CharField(max_length=100)

    a_avg_volume = models.BigIntegerField()

    # Number of consecutive days the stock has been down
    q_consecutive_days_down = models.SmallIntegerField()
    # Total dollar change over the consecutive days down
    a_consecutive_days_price_change = models.DecimalField(max_digits=10, decimal_places=3)
    # Percentage the stock is down (close delta / previous close price)
    q_consecutive_days_percent_change = models.DecimalField(max_digits=10, decimal_places=3)

    # Relation between current share price and the 52 week high
    a_close_to_fifty_two_week_high = models.DecimalField(max_digits=10, decimal_places=3)
    # Relation between current share price and the 52 week low
    a_close_to_fifty_two_week_low = models.DecimalField(max_digits=10, decimal_places=3)

    # Number of consecutive days the volume has grown
    q_consecutive_days_volume_growth = models.SmallIntegerField()
    # Total volume change over the consecutive days
    a_consecutive_days_volume_change = models.BigIntegerField()
    # Percentage the volume has changed
    q_consecutive_days_volume_percent_change = models.DecimalField(max_digits=10, decimal_places=3)

    # a_forward_eps_to_industry =

    class Meta:
        unique_together = ('stockeod', 'd_evaluation')
        ordering = ['-d_evaluation', 'stockeod__stock__n_symbol']

    def __str__(self):
        return str(self.d_evaluation) + " - " + self.stockeod.stock.t_short_name + " [" + self.stockeod.stock.n_symbol + "]"
