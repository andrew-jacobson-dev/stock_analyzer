from django.conf import settings
from django.shortcuts import render
from datetime import date
from django.db import IntegrityError
from django.db.models import F
from stock_summary.models import Stock, StockEOD, StockEODProfile, StockRecommendation
from registration.models import UserStock, UserStockTransaction, UserProfile
from stock_summary.forms import AddTransactionForm, NotificationSettingsForm
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from data_pull.management.commands import pull_basic_stock_info


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def stock_summary_index(request):

    # Get needed dates
    most_recent_close_date = StockEOD.objects.latest('d_process')
    most_recent_close_date = most_recent_close_date.d_process
    today = date.today()

    # Get the current user
    user = request.user
    user_id = request.user.id

    # Create the form for adding stocks
    add_transaction_form = AddTransactionForm(user_id)
    notification_settings_form = NotificationSettingsForm(user_id)

    ####################################################################################################################
    # Get the list of the user's stocks - used for all information on the page!
    stocks_user_data = UserStock.objects.filter(user__id=user_id)

    user_stocks_ids = []
    user_stocks_shares = {}
    user_stocks_invested = {}

    for stock in stocks_user_data:
        user_stocks_ids.append(stock.stock_id)
    ####################################################################################################################
    # Get the list of the user's stocks that they own from the previously created list of all of their stocks
    stocks_owned_user_data = stocks_user_data.filter(user__id=user_id, t_stock_type='OWN')

    # Create list with the stock ids; calculate user's total investment and total number of shares
    user_stocks_owned_ids = []
    user_stocks_owned_ids_invested = {}
    user_stocks_owned_invested = 0
    user_stocks_owned_ids_shares = {}
    user_stocks_owned_shares = 0

    for stock in stocks_owned_user_data:
        user_stocks_owned_ids.append(stock.stock_id)
        user_stocks_owned_ids_invested[stock.stock_id] = stock.a_invested
        user_stocks_owned_invested += stock.a_invested
        user_stocks_owned_ids_shares[stock.stock_id] = stock.q_shares_owned
        user_stocks_owned_shares += stock.q_shares_owned

    # Get the most recent EOD data and basic stock info for the stocks
    stocks_owned_data = StockEOD.objects.filter(stock__id__in=user_stocks_owned_ids, d_process=most_recent_close_date).select_related('stock').order_by('stock__n_symbol')

    user_stocks_owned_value = 0

    for stock in stocks_owned_data:
        stock_close_value = stock.a_close
        user_shares = user_stocks_owned_ids_shares[stock.stock_id]
        user_stocks_owned_value += (stock_close_value * user_shares)

    user_stocks_owned_value = round(user_stocks_owned_value, 3)
    ####################################################################################################################
    # Get the list of the user's stocks that they mock own from the previously created list of all of their stocks
    stocks_mock_owned_user_data = stocks_user_data.filter(user__id=user_id, t_stock_type='MOCK OWN')

    # Create list with the stock ids; calculate user's total investment and total number of shares
    user_stocks_mock_owned_ids = []
    user_stocks_mock_owned_ids_invested = {}
    user_stocks_mock_owned_invested = 0
    user_stocks_mock_owned_ids_shares = {}
    user_stocks_mock_owned_shares = 0

    for stock in stocks_mock_owned_user_data:
        user_stocks_mock_owned_ids.append(stock.stock_id)
        user_stocks_mock_owned_ids_invested[stock.stock_id] = stock.a_invested
        user_stocks_mock_owned_invested += stock.a_invested
        user_stocks_mock_owned_ids_shares[stock.stock_id] = stock.q_shares_owned
        user_stocks_mock_owned_shares += stock.q_shares_owned

    # Get the most recent EOD data and basic stock info for the stocks
    stocks_mock_owned_data = StockEOD.objects.filter(stock__id__in=user_stocks_mock_owned_ids, d_process=most_recent_close_date).select_related('stock').order_by('stock__n_symbol')

    user_stocks_mock_owned_value = 0

    for stock in stocks_mock_owned_data:
        stock_close_value = stock.a_close
        user_shares = user_stocks_mock_owned_ids_shares[stock.stock_id]
        user_stocks_mock_owned_value += (stock_close_value * user_shares)

    user_stocks_mock_owned_value = round(user_stocks_mock_owned_value, 3)
    ####################################################################################################################
    # Get the list of the user's stocks that they are watching
    stocks_watching_user_data = stocks_user_data.filter(user__id=user_id, t_stock_type='WATCH')

    # Create list with the stock ids
    user_stocks_watching_ids = []

    for stock in stocks_watching_user_data:
        user_stocks_watching_ids.append(stock.stock_id)

    # Get the most recent EOD data and basic stock info for the stocks
    stocks_watching_data = StockEOD.objects.filter(stock__id__in=user_stocks_watching_ids, d_process=most_recent_close_date).select_related('stock').order_by('a_close_delta')
    ####################################################################################################################
    # Get alerts
    stock_alerts_buy = []
    stock_alerts_sell = []
    stock_alerts_other = []

    user_stock_profiles = StockEODProfile.objects.select_related('stockeod').filter(d_evaluation=most_recent_close_date)

    for stock_profile in user_stock_profiles:

        if stock_profile.t_status == 'buy':
            stock_alerts_buy.append(stock_profile)
        elif stock_profile.t_status == 'sell' and stock_profile.stockeod.stock.id in user_stocks_owned_ids:
            stock_alerts_sell.append(stock_profile)
        else:
            stock_alerts_other.append(stock_profile)

    stock_alerts_buy_count = len(stock_alerts_buy)
    stock_alerts_sell_count = len(stock_alerts_sell)
    stock_alerts_other_count = len(stock_alerts_other)
    ####################################################################################################################
    # Get the 5 recent transactions by the user
    recent_transactions = UserStockTransaction.objects.filter(userstock__user__id=user_id).select_related('userstock__stock').order_by('-s_transaction')[:5]
    ####################################################################################################################
    # Get any stock recommendations for the user's stocks
    stock_recommendations = StockRecommendation.objects.filter(s_recommendation__date=most_recent_close_date).select_related('stock').order_by('t_to_grade', 'stock__n_symbol', 't_firm')
    buy_recommendations = stock_recommendations.filter(t_to_grade='buy')
    sell_recommendations = stock_recommendations.filter(t_to_grade='sell')
    other_recommendations = stock_recommendations.exclude(t_to_grade__in=('buy','sell'))
    ####################################################################################################################

    if request.method == 'POST':

        if "add-transaction" in request.POST:

            add_transaction_form = AddTransactionForm(user_id, request.POST)

            if add_transaction_form.is_valid():

                # Get the stock that the user selected; if it's not in the system yet, add it
                if add_transaction_form.cleaned_data['ticker_symbol_text']:

                    selected_ticker_symbol = add_transaction_form.cleaned_data['ticker_symbol_text'].upper()

                    try:
                        selected_stock = Stock.objects.get(n_symbol=selected_ticker_symbol)

                    except Stock.DoesNotExist:

                        # If the stock has not yet been added to the system
                        try:
                            # Get the basic stock information for the stock
                            call_command('pull_basic_stock_info', selected_ticker_symbol)

                            # Now get the newly inserted object
                            selected_stock = Stock.objects.get(n_symbol=selected_ticker_symbol)

                            # Fetch historical data for that stock
                            # TODO this needs to update a table that a cron job checks and runs every x minutes
                            # TODO which saves us from having to wait for it finish
                            try:
                                call_command('pull_historical_stock_info', selected_ticker_symbol)

                            except Exception as e:
                                messages.error(request,
                                               'error getting the historical data for ' + selected_ticker_symbol,
                                               extra_tags='danger')
                                print(e)
                                return HttpResponseRedirect('/summary')

                        except Exception as e:
                            messages.error(request, 'error getting the basic data for ' + selected_ticker_symbol,
                                           extra_tags='danger')
                            print(e)
                            return HttpResponseRedirect('/summary')
                else:
                    selected_stock_id = add_transaction_form.cleaned_data['ticker_symbol_choice'].stock_id

                    try:
                        selected_stock = Stock.objects.get(id=selected_stock_id)

                    except Exception as e:
                        messages.error(request, 'error retrieving data for that stock', extra_tags='danger')
                        print(e)
                        return HttpResponseRedirect('/summary')
                # end if

                try:
                    ########################################################################################################
                    # Get the desired action from the form (e.g. watch, own, analyze)
                    transaction_choice = int(add_transaction_form.cleaned_data['transaction_choice_field'])

                    # Get list of possible action values from the form class
                    all_transaction_choices = add_transaction_form.get_transaction_choices()

                    # Find which value in the list of possible values it is
                    transaction_choice = all_transaction_choices[transaction_choice][1]
                    # TODO: clear out values for shares, share price, and investment total if not buy or sell
                    # Determine how to update the UserStock field
                    if transaction_choice == 'watch':
                        userstock_t_stock_type = 'WATCH'

                    elif transaction_choice == 'buy':
                        userstock_t_stock_type = 'OWN'

                    elif transaction_choice == 'mock buy':
                        userstock_t_stock_type = 'MOCK OWN'

                    elif transaction_choice == 'sell':
                        userstock_t_stock_type = 'OWN'

                    elif transaction_choice == 'mock sell':
                        userstock_t_stock_type = 'MOCK OWN'

                    else:
                        userstock_t_stock_type = 'ANALYZE'
                    ########################################################################################################
                    # Evaluate the following fields that are only for buy, sell transactions
                    if add_transaction_form.cleaned_data['shares']:
                        shares = float(add_transaction_form.cleaned_data['shares'])

                        if transaction_choice == 'sell' or transaction_choice == 'mock sell':
                            shares = shares * -1
                    else:
                        shares = None

                    if add_transaction_form.cleaned_data['share_price']:
                        share_price = float(add_transaction_form.cleaned_data['share_price'])
                    else:
                        share_price = None

                    if add_transaction_form.cleaned_data['total_amount']:
                        total_amount = float(add_transaction_form.cleaned_data['total_amount'])

                        if transaction_choice == 'sell' or transaction_choice == 'mock sell':
                            total_amount = total_amount * -1
                    else:
                        total_amount = None
                    ########################################################################################################
                    # Determine UserStock object values
                    userStock_user = user
                    userStock_stock = selected_stock
                    # userstock_t_stock_type = userstock_t_stock_type
                    userStock_q_shares_owned = shares
                    userStock_a_invested = total_amount

                    # Create UserStock object
                    userStock_record = UserStock(
                        user=userStock_user,
                        stock=userStock_stock,
                        t_stock_type=userstock_t_stock_type,
                        q_shares_owned=userStock_q_shares_owned,
                        a_invested=userStock_a_invested,
                    )

                    if insert_UserStock(userStock_record):

                        # Determine UserStockTransaction object values

                        # Get the newly inserted UserStock object
                        userStockTransaction_userstock = UserStock.objects.get(user=userStock_user, stock=userStock_stock)

                        # Get the current StockEODProfile object at the time of insert
                        userStockTransaction_stockeodprofile = StockEODProfile.objects.filter(stockeod__stock=userStock_stock).order_by('-d_evaluation')
                        userStockTransaction_stockeodprofile = userStockTransaction_stockeodprofile.first()

                        # Calculate transaction time
                        userStockTransaction_s_transaction = datetime.now()

                        # Determine date of transaction execution, if not specified by the form
                        if add_transaction_form.cleaned_data['date_executed']:
                            userStockTransaction_d_executed = add_transaction_form.cleaned_data['date_executed']
                        else:
                            userStockTransaction_d_executed = today

                        # Determine the transaction type
                        if transaction_choice == 'watch':
                            userStockTransaction_t_transaction_type = 'WATCH'
                        elif transaction_choice == 'buy':
                            userStockTransaction_t_transaction_type = 'BUY'
                        elif transaction_choice == 'mock buy':
                            userStockTransaction_t_transaction_type = 'MOCK BUY'
                        elif transaction_choice == 'sell':
                            userStockTransaction_t_transaction_type = 'SELL'
                        elif transaction_choice == 'mock sell':
                            userStockTransaction_t_transaction_type = 'MOCK SELL'
                        else:
                            userStockTransaction_t_transaction_type = 'ANALYZE'

                        userStockTransaction_q_shares = shares
                        userStockTransaction_a_share_price = share_price
                        userStockTransaction_a_invested = total_amount
                        userStockTransaction_t_notes = add_transaction_form.cleaned_data['user_notes']

                        # Create UserStockTransaction object
                        userStockTransaction_record = UserStockTransaction(
                            userstock=userStockTransaction_userstock,
                            stockeodprofile=userStockTransaction_stockeodprofile,
                            s_transaction=userStockTransaction_s_transaction,
                            d_executed=userStockTransaction_d_executed,
                            t_transaction_type=userStockTransaction_t_transaction_type,
                            q_shares=userStockTransaction_q_shares,
                            a_share_price=userStockTransaction_a_share_price,
                            a_invested=userStockTransaction_a_invested,
                            t_notes=userStockTransaction_t_notes,
                        )

                        userStockTransaction_record.save()

                    else:
                        messages.error(request, 'error processing transaction', extra_tags='danger')

                except Exception as e:
                    messages.error(request, 'error processing transaction', extra_tags='danger')
                    print(e)

                finally:
                    return HttpResponseRedirect('/summary')

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
                    return HttpResponseRedirect('/summary')

    context = {
        'user_stocks_owned_invested': user_stocks_owned_invested,
        'user_stocks_owned_value': user_stocks_owned_value,
        'user_stocks_owned_ids_shares': user_stocks_owned_ids_shares,
        'user_stocks_owned_shares': user_stocks_owned_shares,
        'user_stocks_owned_ids_invested': user_stocks_owned_ids_invested,

        'user_stocks_mock_owned_invested': user_stocks_mock_owned_invested,
        'user_stocks_mock_owned_value': user_stocks_mock_owned_value,
        'user_stocks_mock_owned_ids_shares': user_stocks_mock_owned_ids_shares,
        'user_stocks_mock_owned_shares': user_stocks_mock_owned_shares,
        'user_stocks_mock_owned_ids_invested': user_stocks_mock_owned_ids_invested,

        'most_recent_close_date': most_recent_close_date,

        'stock_alerts_buy': stock_alerts_buy,
        'stock_alerts_sell': stock_alerts_sell,
        'stock_alerts_other': stock_alerts_other,
        'stock_alerts_buy_count': stock_alerts_buy_count,
        'stock_alerts_sell_count': stock_alerts_sell_count,
        'stock_alerts_other_count': stock_alerts_other_count,

        'recent_transactions': recent_transactions,

        'stock_recommendations': stock_recommendations,
        'buy_recommendations': buy_recommendations,
        'sell_recommendations': sell_recommendations,
        'other_recommendations': other_recommendations,

        'add_transaction_form': add_transaction_form,
        'notification_settings_form': notification_settings_form,

        'stocks_owned_data': stocks_owned_data,
        'stocks_mock_owned_data': stocks_mock_owned_data,
        'stocks_watching_data': stocks_watching_data,
    }

    return render(request, 'stock_summary_index.html', context)


def insert_UserStock(insert_record):

    insert_successful = False

    # Try saving/inserting the object
    try:
        insert_record.save()
        insert_successful = True

    # Check if the user has already added the stock
    # TODO: validate that the user has shares before removing them
    except IntegrityError as e:

        try:
            UserStock.objects.filter(user=insert_record.user, stock=insert_record.stock).update(
                t_stock_type=insert_record.t_stock_type,
                q_shares_owned=F('q_shares_owned') + insert_record.q_shares_owned,
                a_invested=F('a_invested') + insert_record.a_invested,
            )
            insert_successful = True

        except Exception as e:
            print(e)
            insert_successful = False

    except Exception as e:
        print(e)
        insert_successful = False

    return insert_successful
