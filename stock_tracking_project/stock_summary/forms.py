from django import forms
from django.contrib.auth.models import User
from registration.models import UserStock, UserProfile


class AddTransactionForm(forms.Form):

    transaction_choices = [('0', 'watch'), ('1', 'buy'), ('2', 'mock buy'), ('3', 'sell'), ('4', 'mock sell'),
                           ('5', 'analyze')]

    transaction_choice_field = forms.ChoiceField(
        choices=transaction_choices,
        initial='0',
        label="action",
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )

    ticker_symbol_text = forms.CharField(
        max_length=5,
        label="ticker symbol",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. AAPL",
        })
    )

    ticker_symbol_choice = forms.ModelChoiceField(
        queryset=None,
        label="stock",
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )

    date_executed = forms.DateField(
        label="date executed",
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control",
        })
    )

    user_notes = forms.CharField(
        max_length=100,
        label="notes",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "optional",
            "rows": 2,
        })
    )

    ####################################################################################################################
    # Only for buy, mock buy, sell, mock sell

    shares = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        label="shares",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0.00",
        })
    )

    share_price = forms.DecimalField(
        max_digits=8,
        decimal_places=3,
        required=False,
        label="share price",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "$ 0.00",
        })
    )

    total_amount = forms.DecimalField(
        max_digits=8,
        decimal_places=3,
        required=False,
        label="total amount",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "$ 0.00",
        })
    )
    ####################################################################################################################

    def get_transaction_choices(self):

        return self.transaction_choices

    def __init__(self, user_id, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['ticker_symbol_choice'].queryset = UserStock.objects.filter(user__id=user_id).select_related('stock').order_by('stock__t_short_name')

    class Meta:
        model = UserStock
        fields = ['ticker_symbol_choice']


class NotificationSettingsForm(forms.Form):

    expert_rec_send_email = forms.BooleanField(
        label="send emails",
        required=False,
    )

    expert_rec_send_text = forms.BooleanField(
        label="send texts",
        required=False,
    )

    expert_rec_buy = forms.BooleanField(
        label="buy",
        required=False,
    )

    expert_rec_sell = forms.BooleanField(
        label="sell",
        required=False,
    )

    expert_rec_other = forms.BooleanField(
        label="other",
        required=False,
    )

    custom_alerts_send_email = forms.BooleanField(
        label="send emails",
        required=False,
    )

    custom_alerts_send_text = forms.BooleanField(
        label="send texts",
        required=False,
    )

    custom_alerts_buy = forms.BooleanField(
        label="buy",
        required=False,
    )

    custom_alerts_sell = forms.BooleanField(
        label="sell",
        required=False,
    )

    custom_alerts_other = forms.BooleanField(
        label="other",
        required=False,
    )

    def __init__(self, user_id, *args, **kwargs):

        super(NotificationSettingsForm, self).__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        if user:
            self.fields['expert_rec_send_email'].initial = user.userprofile.i_expert_rec_send_email
            self.fields['expert_rec_send_text'].initial = user.userprofile.i_expert_rec_send_text
            self.fields['expert_rec_buy'].initial = user.userprofile.i_expert_rec_buy
            self.fields['expert_rec_sell'].initial = user.userprofile.i_expert_rec_sell
            self.fields['expert_rec_other'].initial = user.userprofile.i_expert_rec_other
            self.fields['custom_alerts_send_email'].initial = user.userprofile.i_custom_alerts_send_email
            self.fields['custom_alerts_send_text'].initial = user.userprofile.i_custom_alerts_send_text
            self.fields['custom_alerts_buy'].initial = user.userprofile.i_custom_alerts_buy
            self.fields['custom_alerts_sell'].initial = user.userprofile.i_custom_alerts_sell
            self.fields['custom_alerts_other'].initial = user.userprofile.i_custom_alerts_other

    class Meta:
        model = UserStock
        fields = ['ticker_symbol_choice']
