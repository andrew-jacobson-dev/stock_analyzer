from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='completely optional. solely used for UI customization.',
        widget=forms.TextInput(attrs={
            "placeholder": "optional",
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='completely optional. solely used for UI customization.',
        widget=forms.TextInput(attrs={
            "placeholder": "optional",
        })
    )

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # def clean_username(self):
    #
    #     username = self.cleaned_data['username'].lower()
    #     r = User.objects.filter(username=username)
    #
    #     if r.count():
    #         raise ValidationError("Username already exists")
    #
    #     return username
    #
    # def clean_email(self):
    #
    #     email = self.cleaned_data['email'].lower()
    #     r = User.objects.filter(email=email)
    #
    #     if r.count():
    #         raise ValidationError("Email already exists")
    #
    #     return email
    #
    # def clean_password2(self):
    #
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Password don't match")
    #
    #     return password2
    #
    # def save(self, commit=True):
    #
    #     user = User.objects.create_user(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email'],
    #         self.cleaned_data['password1']
    #     )
    #
    #     return user


class EditUserForm(UserChangeForm):


    def __init__(self, user_id, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        current_user = User.objects.get(id=user_id)
        self.fields['first_name'].initial = current_user.first_name
        self.fields['last_name'].initial = current_user.last_name
        self.fields['email'].initial = current_user.email
        self.fields['username'].initial = current_user.username