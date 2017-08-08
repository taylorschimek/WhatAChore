import datetime
import json
from datetime import date

from django.contrib import messages
from django.contrib.auth import views as authviews
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, get_user_model, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.utils import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.views.generic.edit import FormMixin

from django.contrib.auth.views import password_reset

from whatachore.tasks import pw_email, user_to_worker

from wac.forms import PersonEditForm, ChoreEditForm
from .forms import AccountSettingsForm, EmailLoginForm, EmailWorkerForm, RegistrationForm, PasswordResetRequestForm

from wac.views import PersonCreateView, ChoreCreateView
from wac.models import Assignment, Person, User, Week
from .models import User


def my_password_reset(request):
    if request.is_ajax() and request.method == 'POST':
        form = PasswordResetRequestForm(data=request.POST)
        email = []
        if form.is_valid():
            email.append(form.cleaned_data['email'])
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            pw_email.delay(email, token)
            messages.success(request, 'An email has been sent to ' + email +".  Please check your inbox to continue resetting your password.")

            response_data = {}
            response_data['status'] = 'success'
            response_data['url'] = 'landing'

            return HttpResponse(json.dumps(response_data),
                content_type='application/json')
            # return render(request, 'registration/password_reset_done.html')
        else:
            print("FUCKING FORM ISN'T VALID")
    else:
        form = PasswordResetRequestForm()
        return render(request, 'registration/password_reset_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = get_user_model().objects._create_user(**form.cleaned_data)
            login(request, new_user)
            return HttpResponseRedirect('../welcome')
        else:
            return render(request, 'landing.html', {'form': form})
    else:
        form = RegistrationForm()
        return HttpResponseRedirect(reverse('landing'))



class WelcomeOneView(PersonCreateView):
    template_name = 'welcomeNew.html'

    def get(self, request, *args, **kwargs):
        theUser = request.user
        form = PersonEditForm(initial={'email': theUser.email,})

        return render(request, 'useraccounts/welcomeNew.html', {'form': form})


class WelcomeTwoView(TemplateView):
    template_name = 'welcomeNew2.html'


class WelcomeLastView(TemplateView):
    template_name = 'welcomeNewLast.html'


class HomeView(TemplateView):
    model = User
    template_name = 'home.html'

    def get(self, request):
        user = self.request.user
        if user.is_authenticated():
            # self.profiled()
            return render(request, self.template_name, self.get_context_data())
        else:
            messages.warning(request, "Please log in or create an account.")
            return HttpResponseRedirect(reverse('landing'))

    def profiled(self):
        theUser = Person.objects.filter(
            user = self.request.user
        ).filter(
            email__exact=self.request.user.email
        )
        if len(theUser):
            print("BINGO")
            return theUser[0].name
        else:
            print("BONGO")
            return self.request.user.email

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


def email_to_worker(request):
    template_name = 'email_worker_modal.html'
    if request.is_ajax() and request.method == 'POST':
        print("AJAX")
        form = EmailWorkerForm(data=request.POST)
        if form.is_valid():
            print("VALID")
            # gather email pieces
            recipient_list = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # call email task
            user_to_worker.delay(recipient_list, subject, message)

            messages.success(request, "Your email is on its way.")
            response_data = {}
            response_data['status'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            print("INVALID")
            response_data = {}
            response_data['status'] = 'fail'
            return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")
    else:
        recipient_list = ''
        person_pk = request.GET.get('person')
        if person_pk:
            print(person_pk)
            worker = Person.objects.get(pk=person_pk)
            recipient_list.append(worker.email)
            print(worker)
            print("worker.email = {}".format(worker.email))
            form = EmailWorkerForm()
            if worker.email:
                form = EmailWorkerForm(initial={'recipient_email': worker.email})
                print("GET")
                return render(request, template_name, {'form': form})
            else:
                print("That particular worker doesn't have an email address on file.")
                messages.warning(request, "Looks like that worker doesn't have an email address on file.")
                return render(request, template_name, {'form': form})
        else:
            print("no person_pk so ALL")
            messages.info(request, "Emails will only be sent to workers with an email address on file.")
            # get all workers
            workers = Person.objects.filter(
                user = request.user
            ).exclude(
                email = None
            )
            print(workers)
            for worker in workers:
                recipient_list += worker.email + ', '

            # set recipient email field to list of all emails.
            form = EmailWorkerForm(initial={'recipient_email': recipient_list})
            return render(request, template_name, {'form': form})



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
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print("USER DONOTEMAIL VALUE = {}".format(user.doNotEmail))
        form = AccountSettingsForm(initial={
            'no_email': user.doNotEmail
        })
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, *args, **kwargs):
        print("POSTING")
        form = AccountSettingsForm(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print("FORM VALID")
        user = self.request.user
        no_email_value = form.cleaned_data['no_email']
        user.doNotEmail = no_email_value
        user.save(update_fields=['doNotEmail'])
        return HttpResponse(reverse('home-view'))

    def form_invalid(self, form):
        print("FORM INVALID")


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
        return super(EmailLoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        form = EmailLoginForm(request)
        return render(request, 'useraccounts/registration/login.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = EmailLoginForm(request, data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login(self.request, form.get_user())
        response_data = {}
        response_data['status'] = 'success'
        response_data['url'] = '/useraccounts/home'
        response_data['email'] = self.request.user.email
        return HttpResponse(json.dumps(response_data),
            content_type='application/json')

    def form_invalid(self, form):
        response_data = {}
        response_data['status'] = 'fail'
        return HttpResponseBadRequest(json.dumps(form.errors), content_type='application/json')


def login_page(request):
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login(request, form.get_user())
            response_data = {}
            response_data['status'] = 'success'
            response_data['url'] = '/useraccounts/home'
            return HttpResponse(json.dumps(response_data),
                content_type='application/json')
        else:
            response_data = {}
            response_data['status'] = 'fail'
            return HttpResponseBadRequest(json.dumps(form.errors), content_type='application/json')
    else:
        form = EmailLoginForm()
    return render(request, 'useraccounts/login_page.html', context={'form': form})



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
        form = PasswordChangeForm(user=self.request.user)
        return render(request, 'useraccounts/registration/password_change_form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        user = self.request.user
        if form.is_valid():
            return self.form_valid(user, form)
        else:
            return self.form_invalid(form)

    def form_valid(self, user, form):
        new_pass = form.cleaned_data['new_password1']
        user.set_password(new_pass)
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Your password was updated successfully!")

        response_data = {}
        response_data['status'] = 'success'
        # response_data['messages'] = 'Your password was updated successfully'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def form_invalid(self, form):
        response_data = {}
        response_data['status'] = 'fail'
        return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")


def change_password_done(request):
    return HttpResponseRedirect(reverse('home-view'))
