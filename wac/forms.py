from django import forms

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

    class Meta:
        model = models.Person
        fields = [
            'name',
            'age',
            'phone_number',
            'email',
            'day_off',
            'pic_location'
        ]
