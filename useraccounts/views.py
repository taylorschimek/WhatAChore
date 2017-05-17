from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView, FormView

from wac.forms import PersonEditForm

from .forms import RegistrationForm

from wac.views import PersonCreateView

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = get_user_model().objects._create_user(**form.cleaned_data)
            login(request, new_user)
            return HttpResponseRedirect('../welcome')
        else:
            return HttpResponse('errors')
    else:
        form = RegistrationForm()

    return render(request, 'landing')


class ProfileCreateFormView(PersonCreateView):
    template_name = 'welcomeNew.html'
