from django import forms

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
    }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter email'}
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
