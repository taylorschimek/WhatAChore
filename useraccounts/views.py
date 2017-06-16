import datetime
import json
from datetime import date

from django.contrib import messages
from django.contrib.auth import views as authviews
from django.conf import settings
from django.forms.utils import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormMixin

from wac.forms import PersonEditForm
from .forms import EmailLoginForm, RegistrationForm

from wac.views import PersonCreateView
from wac.models import Assignment, Person, User, Week
from .models import User


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

    def get(self, request, *args, **kwargs):
        theUser = request.user
        form = PersonEditForm(initial={'email': theUser.email,})

        return render(request, 'useraccounts/welcomeNew.html', {'form': form})




class HomeView(TemplateView):
    model = User
    template_name = 'home.html'

    def profiled(self):
        theUser = Person.objects.filter(
            user = self.request.user
        ).filter(
            email__exact=self.request.user.email
        )
        print(theUser)
        return theUser[0]

    def get_context_data(self, **kwargs):
        current_day = date.today()

        context = super(HomeView, self).get_context_data(**kwargs)

        context['people'] = Person.objects.filter(
            user = self.request.user
        )

        context['assignments'] = Assignment.objects.filter(
            week__user = self.request.user
        ).filter(
            week__is_current = True
        ).filter(
            when = current_day
        )

        context['not_done'] = Assignment.objects.filter(
            week__user = self.request.user
        ).filter(
            week__is_current = True
        ).filter(
            when__lt=current_day
        ).filter(
            done = False
        ).order_by("when")

        context['old_weeks'] = Week.objects.filter(
            user = self.request.user
        ).exclude(
            is_current = True
        )

        return context


class OldWeekView(DetailView):
    model = Week
    template_name = 'passed_week_modal.html'

    def get_context_data(self, **kwargs):
        context = super(OldWeekView, self).get_context_data(**kwargs)

        context['assignments'] = Assignment.objects.filter(
            week__pk=kwargs['object'].pk
        ).order_by("when")

        start_date = kwargs['object'].start_date

        context['dates'] = []

        for i in range(0,7):
            context['dates'].append(start_date+datetime.timedelta(days=i))

        return context


class AccountSettings(TemplateView):
    model = User
    template_name = 'account_settings.html'

    def get_context_data(self, **kwargs):
        context = super(AccountSettings, self).get_context_data(**kwargs)

        context['user'] = self.request.user

        print(kwargs)
        print(context['user'])

        return context


# def ajax_login(request):
#     form = AuthenticationForm()
#     print(form)
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         print(request.POST)
#
#         if form.is_valid():
#             print("VALID")
#             login(request, form.get_user())
#             return HttpResponse(json.dumps({'success': 'ok'}),
#                 mimetype='application/json')
#         else:
#             print("INVALID")
#             return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")
#     return render(request, 'useraccounts/registration/login.html', {'form': form})



class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)



class EmailLoginView(AjaxTemplateMixin, TemplateView, authviews.LoginView):
    template_name = 'useraccounts/registration/login.html'
    form_class = EmailLoginForm

    def dispatch(self, request, *args, **kwargs):
        print("DISPATCH")
        return super(EmailLoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        print("GET")
        form = EmailLoginForm(request)
        return render(request, 'useraccounts/registration/login.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        print("POST")
        form = EmailLoginForm(request, data=self.request.POST)
        print(form.data)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print("VALID")
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login(self.request, form.get_user())
        response_data = {}
        response_data['status'] = 'success'
        response_data['url'] = '/useraccounts/home'
        return HttpResponse(json.dumps(response_data),
            content_type='application/json')

    def form_invalid(self, form):
        print("INVALID")
        response_data = {}
        response_data['status'] = 'fail'
        return HttpResponseBadRequest(json.dumps(form.errors), content_type='application/json')



class ChangePasswordView(FormMixin, AjaxTemplateMixin, TemplateView):
    template_name = 'useraccounts/registration/password_change_form.html'
    form_class = PasswordChangeForm

    def dispatch(self, request, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        print("GET")
        form = PasswordChangeForm(user=self.request.user)
        return render(request, 'useraccounts/registration/password_change_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        print("POST")
        print(self.request.POST)
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        user = self.request.user
        if form.is_valid():
            return self.form_valid(user, form)
        else:
            return self.form_invalid(form)

    def form_valid(self, user, form):
        print("VALID")
        new_pass = form.cleaned_data['new_password1']
        user.set_password(new_pass)
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Your password was updated successfully!")

        response_data = {}
        response_data['status'] = 'success'
        response_data['messages'] = 'Your password was updated successfully'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def form_invalid(self, form):
        print("INVALID")
        response_data = {}
        response_data['status'] = 'fail'
        return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")

def change_password_done(request):
    return HttpResponseRedirect(reverse('home-view'))
