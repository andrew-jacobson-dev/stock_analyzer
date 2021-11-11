from django.db import models


# Create your models here.
class NYSEHoliday(models.Model):

    d_holiday = models.DateField()
    t_holiday = models.CharField(max_length=100)

    class Meta:
        ordering = ['-d_holiday']

    def __str__(self):
        return str(self.d_holiday) + " (" + self.t_holiday + ")"


class JobRun(models.Model):

    s_run = models.DateTimeField(auto_now_add=True)
    t_job_name = models.CharField(max_length=60)
    t_script_name = models.CharField(max_length=60)
    t_status = models.CharField(max_length=30)
    t_message = models.CharField(max_length=100)

    class Meta:
        ordering = ['-s_run', 't_job_name']

    def __str__(self):
        return str(self.s_run) + " - " + self.t_job_name + " - " + self.t_status
