from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from data_pull.models import JobRun
from datetime import date, datetime, timedelta


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def jobs_index(request):

    # Get the recent job runs
    one_week_ago = datetime.now().date() - timedelta(7)
    job_runs = JobRun.objects.filter(s_run__date__gte=one_week_ago).order_by('-s_run')

    context = {
        'job_runs': job_runs
    }

    return render(request, 'jobs_index.html', context)