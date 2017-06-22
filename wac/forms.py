from django import forms
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from . import models
from .widgets import CustomClearableFileInput


class AssignmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Assignment
        fields = [
            'who',
            'when'
        ]


class ChoreEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChoreEditForm, self).__init__(*args, **kwargs)
        self.fields['interval'].widget.attrs['class'] = 'hideController'
        self.fields['sub_interval'].widget.attrs['class'] = 'hiddenSub'

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
        help_texts = {
            'duration': _('in minutes, please.'),
        }


class PersonEditForm(forms.ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
            self.fields['name'].required = True
            self.fields['birthday'].required = True
            self.fields['day_off'].required = True

        # print(kwargs)
        #
        # if 'initial' in kwargs:
        #     if kwargs['initial']['mugshot']:
        #         print("True")
        #         self.fields['mugshot'].widget.is_initial(False)
        #     else:
        #         print("False")
        #         self.fields['mugshot'].widget.is_initial(True)


    class Meta:
        model = models.Person
        fields = [
            'name',
            'birthday',
            'phone_number',
            'email',
            'day_off',
            'mugshot',
            'x',
            'y',
            'width',
            'height',
        ]
        help_texts = {
            'birthday': _('YYYY-MM-DD - used only to assign correct chores to younger workers.'),
            'day_off': _('Specific day a worker would rather not or cannot have chores.')
        }
        widgets = {'mugshot': CustomClearableFileInput}

    def crop_image(self):
        print("Crop Happened")
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(self.cleaned_data['mugshot'])
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((300, 400), Image.ANTIALIAS)
        return resized_image
