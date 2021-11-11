from django.db import models
from django.contrib.auth.models import User
from stock_summary.models import Stock, StockEODProfile
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)

    instance.userprofile.save()


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    t_phone_number = models.CharField(max_length=15, null=True)
    i_summary_pg_alerts_open = models.BooleanField(null=True, default=True)
    i_summary_pg_trans_open = models.BooleanField(null=True, default=True)
    i_summary_pg_port_open = models.BooleanField(null=True, default=True)
    i_expert_rec_send_email = models.BooleanField(null=True)
    i_expert_rec_send_text = models.BooleanField(null=True)
    i_expert_rec_buy = models.BooleanField(null=True)
    i_expert_rec_sell = models.BooleanField(null=True)
    i_expert_rec_other = models.BooleanField(null=True)
    i_custom_alerts_send_email = models.BooleanField(null=True)
    i_custom_alerts_send_text = models.BooleanField(null=True)
    i_custom_alerts_buy = models.BooleanField(null=True)
    i_custom_alerts_sell = models.BooleanField(null=True)
    i_custom_alerts_other = models.BooleanField(null=True)

    def __str__(self):
        return self.user.username


class UserStock(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    d_added = models.DateField(auto_now_add=True)
    # W, O, MO, A
    t_stock_type = models.CharField(max_length=10)
    q_shares_owned = models.DecimalField(max_digits=9, decimal_places=6, default=0, null=True)
    a_invested = models.DecimalField(max_digits=8, decimal_places=3, default=0, null=True)

    class Meta:
        unique_together = ('user', 'stock')
        ordering = ['user__username', 'stock__t_short_name']

    def __str__(self):
        return self.stock.t_short_name + " [" + self.stock.n_symbol + "]"


class UserStockTransaction(models.Model):

    userstock = models.ForeignKey(UserStock, on_delete=models.CASCADE)
    stockeodprofile = models.ForeignKey(StockEODProfile, on_delete=models.CASCADE, blank=True, null=True)
    s_transaction = models.DateTimeField()
    d_executed = models.DateField(null=True)
    t_transaction_type = models.CharField(max_length=10)
    q_shares = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    a_share_price = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    a_invested = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    t_notes = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('userstock', 's_transaction')
        ordering = ['s_transaction', 'userstock__user__username']

    def __str__(self):
        return self.userstock.stock.t_short_name + " [" + self.userstock.stock.n_symbol + "]"


class UserStockAlert(models.Model):

    userStock = models.ForeignKey(UserStock, on_delete=models.CASCADE)
    d_alert = models.DateField(auto_now_add=True)
    t_alert = models.CharField(max_length=100)

    def __str__(self):
        return "[" + self.stock.n_symbol + "] " + self.t_alert
