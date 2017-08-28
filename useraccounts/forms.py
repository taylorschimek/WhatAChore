from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from useraccounts.fields import CommaSeparatedEmailField


class RegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
    }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'id': 'reg_password', 'class': 'form-control', 'placeholder': 'Password'}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'id': 'reg_email', 'class': 'form-control', 'placeholder': 'Enter email'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.password)
        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):
    def clean(self):
        try:
            self.cleaned_data['username'] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data['username'] = "a_username_that_do_not_exists_anywhere_in_the_site"

        return super(EmailLoginForm, self).clean()


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(max_length=254)


class AccountSettingsForm(forms.Form):
    no_email = forms.BooleanField(required=False)


class EmailWorkerForm(forms.Form):
    recipient_email = CommaSeparatedEmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
