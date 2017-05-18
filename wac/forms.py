from django import forms
from django.utils.translation import ugettext_lazy as _


from . import models


class ChoreEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChoreEditForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = models.Chore
        fields = [
            'task',
            'description',
            'duration',
            'interval',
            'sub_interval',
            'age_restriction',
            'chore_icon_location'
        ]


class PersonEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
            self.fields['name'].required = True
            self.fields['birthday'].required = True
            self.fields['day_off'].required = True

    class Meta:
        model = models.Person
        fields = [
            'name',
            'birthday',
            'phone_number',
            'email',
            'day_off',
            'mugshot',
        ]
        help_texts = {
            'birthday': _('YYYY-MM-DD - used only to assign correct chores to younger workers.'),
            'day_off': _('Specific day a worker would rather not or cannot have chores.')
        }
