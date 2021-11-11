from django.db import models


# Create your models here.
class ChartInterval(models.Model):

    n_page_order = models.SmallIntegerField()
    t_short_name = models.CharField(max_length=3)
    t_long_name = models.CharField(max_length=25)
    q_days = models.SmallIntegerField()
    i_active = models.BooleanField()

    class Meta:
        ordering = ['q_days']

    def __str__(self):
        return "[" + self.t_short_name + "] " + self.t_long_name