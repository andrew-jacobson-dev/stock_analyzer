from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from registration.models import UserProfile
from registration.forms import RegistrationForm, EditUserForm
from stock_summary.forms import NotificationSettingsForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def registration_index(request):

    # Create the log in and registration forms
    log_in_form = AuthenticationForm()
    registration_form = RegistrationForm()

    if request.method == 'POST':

        if "log-in" in request.POST:

            registration_form = RegistrationForm()
            log_in_form = AuthenticationForm(request=request, data=request.POST)

            if log_in_form.is_valid():

                log_in_username = log_in_form.cleaned_data.get('username')
                log_in_password = log_in_form.cleaned_data.get('password')
                user = authenticate(username=log_in_username, password=log_in_password)

                if user is not None:

                    login(request, user)
                    return HttpResponseRedirect('/summary')

                else:

                    messages.error(request, 'log in failed')

        if "register" in request.POST:

            registration_form = RegistrationForm(request.POST)
            log_in_form = AuthenticationForm()

            if registration_form.is_valid():

                registration_form.save()
                log_in_username = registration_form.cleaned_data.get('username')
                log_in_password = registration_form.cleaned_data.get('password1')
                user = authenticate(username=log_in_username, password=log_in_password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/summary')
                else:
                    messages.error(request, 'log in failed')

    context = {
        'registration_form': registration_form,
        'log_in_form': log_in_form,
    }

    return render(request, 'registration_index.html', context)


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def profile_index(request):

    # Get the current user
    user = request.user
    user_id = request.user.id

    edit_user_form = EditUserForm(user_id)
    notification_settings_form = NotificationSettingsForm(user_id)

    if request.method == 'POST':

        if "save-user-info" in request.POST:

            edit_user_form = EditUserForm(user_id, request.POST)

            if edit_user_form.is_valid():

                print('here1')

        if "save-notification-settings" in request.POST:

            notification_settings_form = NotificationSettingsForm(user_id, request.POST)

            if notification_settings_form.is_valid():

                userProfile_i_expert_rec_send_email = notification_settings_form.cleaned_data['expert_rec_send_email']
                userProfile_i_expert_rec_send_text = notification_settings_form.cleaned_data['expert_rec_send_text']
                userProfile_i_expert_rec_buy = notification_settings_form.cleaned_data['expert_rec_buy']
                userProfile_i_expert_rec_sell = notification_settings_form.cleaned_data['expert_rec_sell']
                userProfile_i_expert_rec_other = notification_settings_form.cleaned_data['expert_rec_other']
                userProfile_i_custom_alerts_send_email = notification_settings_form.cleaned_data['custom_alerts_send_email']
                userProfile_i_custom_alerts_send_text = notification_settings_form.cleaned_data['custom_alerts_send_text']
                userProfile_i_custom_alerts_buy = notification_settings_form.cleaned_data['custom_alerts_buy']
                userProfile_i_custom_alerts_sell = notification_settings_form.cleaned_data['custom_alerts_sell']
                userProfile_i_custom_alerts_other = notification_settings_form.cleaned_data['custom_alerts_other']

                try:
                    UserProfile.objects.filter(user=user_id).update(
                        i_expert_rec_send_email=userProfile_i_expert_rec_send_email,
                        i_expert_rec_send_text=userProfile_i_expert_rec_send_text,
                        i_expert_rec_buy=userProfile_i_expert_rec_buy,
                        i_expert_rec_sell=userProfile_i_expert_rec_sell,
                        i_expert_rec_other=userProfile_i_expert_rec_other,
                        i_custom_alerts_send_email=userProfile_i_custom_alerts_send_email,
                        i_custom_alerts_send_text=userProfile_i_custom_alerts_send_text,
                        i_custom_alerts_buy=userProfile_i_custom_alerts_buy,
                        i_custom_alerts_sell=userProfile_i_custom_alerts_sell,
                        i_custom_alerts_other=userProfile_i_custom_alerts_other,
                    )

                except Exception as error:
                    print(error)
                    messages.error(request, 'error updating settings', extra_tags='danger')

                finally:
                    return HttpResponseRedirect('/profile')

    context = {
        'edit_user_form': edit_user_form,
        'notification_settings_form': notification_settings_form,
    }

    return render(request, 'profile_index.html', context)
