import calendar
import datetime
import json
import os

from whatachore.tasks import add
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, DeleteView
from django.views.generic.edit import FormMixin
from io import BytesIO

from wac.models import Assignment, Chore, Person, Week

from .forms import AssignmentForm, ChoreEditForm, PersonEditForm

from wac.signals.handlers import single_chore_added

from PIL import Image



#=============== LINEUP ==================#
#=========================================#
def lineup(request):
    # add.delay(3, 5)
    if request.is_ajax():

        # Update done field on assignment
        assignment = Assignment.objects.get(pk=request.POST['pk'])
        people = Person.objects.filter(user=assignment.week.user)
        person = people.get(
            name=assignment.who
        )

        if assignment.done is True:
            assignment.done = False
            person.weekly_minutes += assignment.what.duration
            # person.number_of_chores += 1
        else:
            assignment.done = True
            person.weekly_minutes -= assignment.what.duration
            # person.number_of_chores -= 1
        assignment.save(update_fields=['done'])
        person.save(update_fields=['weekly_minutes'])
        html = render_to_string('wac/assignments_list_sub.html', {'people': people, 'week': assignment.week})
        return HttpResponse(html)
    else:
        try:
            if len(Person.objects.filter(user = request.user)) and len(Chore.objects.filter(user = request.user)):
                new_week = Week.create(current_user=request.user)
                send_mail('test', 'testing this nonsense', 'noreply@taylorschimek.com', ['ruof@yahoo.com'])
            else:
                messages.warning(request, '''You either: \n
                                             1. have no chores or \n
                                             2. have no workers. \n
                                             Assignments cannot be formed.''')
        except ZeroDivisionError:
            messages.warning(request, '''You either: \n
                                         1. have no chores or \n
                                         2. have no workers. \n
                                         Assignments cannot be formed.''')
    return HttpResponseRedirect(reverse('lineup'))


class AssignmentListView(LoginRequiredMixin, TemplateView):
    context_object_name = 'assignments'
    model = Assignment
    template_name = 'wac/assignments_list.html'

    def get_context_data(self, **kwargs):

        # Very first time someone clicks on Assignment page
        weeks = Week.objects.filter(
            user = self.request.user
        )
        if len(weeks) == 0:
            new_week = Week.create(current_user=self.request.user)

        # all subsequent calls to Assignment page
        current_week = weeks.filter(
            user = self.request.user
        ).filter(
            is_current = True
        )

        dates = []

        if len(current_week):
            monday = current_week[0].start_date
            for i in range(7):
                dates.append(monday + datetime.timedelta(days=i))

            context = super(AssignmentListView, self).get_context_data(**kwargs)

            context['people'] = Person.objects.filter(
                user = self.request.user
            ).order_by('name')

            context['assignments'] = Assignment.objects.filter(
                week__user=self.request.user
            ).filter(
                week__is_current=True
            )

            context['dates'] = dates
            context['week'] = current_week[0]

            return context


class AssignmentDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Assignment
    form_class = AssignmentForm

    def dispatch(self, request, *args, **kwargs):
        self.assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        return super(AssignmentDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        form = AssignmentForm(instance=self.assignment,
                              initial={'when': self.assignment.when})
        form.fields['who'].queryset = Person.objects.filter(user=request.user)
        form.fields['who'].initial = self.assignment.who.name
        return render(request, 'wac/assignment_detail.html', {'form': form, 'assignment': self.assignment})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AssignmentForm(request.POST, request.FILES, instance=self.assignment)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.from_invalid(form)

    def form_valid(self, form):
        remove = 'http://localhost:8000/'
        nextFull = self.request.POST['fromUrl'].replace(remove, '')
        if nextFull == 'useraccounts/home/':
            next = 'home-view'
        else:
            next = 'lineup'
        form.save()
        messages.success(self.request, self.object.what.task + ' was updated successfully!')
        return HttpResponseRedirect(reverse(next))

    def form_invalid(self, form):
        return render(self.request, 'wav/assignment_detail.html', {'form': form, 'assignment': self.assignment})






#=============== CHORES ==================#
#=========================================#

class ChoreListView(LoginRequiredMixin, ListView):
    template_name = 'wac/chore_list.html'
    context_object_name = 'chores'
    model = Chore

    def get_queryset(self):
        order = ['Daily', 'Every 2 Days', 'Every 3 Days', 'Weekly', 'Every 2 Weeks', 'Monthly', 'Every 2 Months', 'Quarterly', 'Yearly']
        return sorted(Chore.objects.filter(user=self.request.user).order_by('task'), key = lambda c: order.index(c.interval))



class ChoreCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Chore
    form_class = ChoreEditForm
    template_name_suffix = '_create_form'

    def get(self, request, *args, **kwargs):
        # print('get get get')
        print(settings.STATIC_ROOT)
        print(settings.STATIC_URL)
        initial_icon_location = settings.STATIC_ROOT + '/wac/styles/images/icons/cream_icons/00_Default.png'
        form = ChoreEditForm(initial={'chore_icon_location': initial_icon_location})
        included_extensions = ['png']
        icon_locations = settings.STATIC_ROOT + '/wac/styles/images/icons/red_icons'
        choices = [fn for fn in os.listdir(icon_locations)
                   if any(fn.endswith(ext) for ext in included_extensions)]
        # print("get's choices {}".format(choices))
        paths = choices

        return render(request, 'wac/chore_create_form.html', {'form': form, 'paths': paths})


    def form_valid(self, form):
        print(form.cleaned_data)
        user = self.request.user
        new_chore = form.save(commit=False)
        new_chore.user = user
        new_chore.last_assigned = datetime.date.today()
        # new_chore.chore_icon_location = '/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/Icons/cream_icons/' + form.cleaned_data['chore_icon_location']
        new_chore.save()

        response_data = {}
        response_data['status'] = 'success'

        if user.welcomed:
            print("wac.views.ChoreCreateView.form_valid: welcomed is True")

            # Make assignment if chore.interval is Every 3 Days or more often:
            weekly_or_less = ['Every 3 Days', 'Every 2 Days', 'Daily']
            if new_chore.interval in weekly_or_less:
                weeks = Week.objects.filter(
                    user = self.request.user
                )
                if len(weeks):
                    this_week = weeks.filter(is_current=True)[0]
                    if this_week:
                        single_chore_added(new_chore, this_week)


            response_data['messages'] = '{} has been added to the list.'.format(new_chore.task)
            messages.success(self.request, new_chore.task + " was added successfully!")

        else:
            print("wac.views.ChoreCreateView.form_valid: welcomed is False")
            user.welcomed = True
            user.save(update_fields=['welcomed'])
            response_data = {}
            response_data['status'] = 'success'
            response_data['messages'] = 'welcoming'
            response_data['url'] = reverse('welcome-newLast')

        return HttpResponse(json.dumps(response_data), content_type='application/json')


    def form_invalid(self, form):
        response_data = {}
        response_data['status'] = 'fail'
        return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")


class ChoreDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Chore
    form_class = ChoreEditForm

    def dispatch(self, request, *args, **kwargs):
        self.chore = Chore.objects.get(pk=self.kwargs['pk'])
        return super(ChoreDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        included_extensions = ['png']
        icon_locations = settings.STATIC_ROOT + '/wac/styles/images/icons/red_icons'
        choices = [fn for fn in os.listdir(icon_locations)
                   if any(fn.endswith(ext) for ext in included_extensions)]

        print(choices)

        form = ChoreEditForm(instance=self.chore,
                             initial={'task': self.chore.task,
                                      'duration': self.chore.duration,
                                      'description': self.chore.description,
                                      'interval': self.chore.interval,
                                      'sub_interval': self.chore.sub_interval,
                                      'age_restriction': self.chore.age_restriction,
                                      'last_assigned': self.chore.last_assigned,
                                      'chore_icon_location': self.chore.chore_icon_location})
        return render(request, 'wac/chore_detail.html', {'form': form, 'chore': self.chore, 'paths': choices})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ChoreEditForm(request.POST, instance=self.chore)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.object.task + " was updated successfully!")
        return HttpResponseRedirect(reverse('chore-list'))

    def form_invalid(self, form):
        return render(self.request, 'wac/chore_detail.html', {'form': form, 'chore': self.chore})


class ChoreDelete(LoginRequiredMixin, DeleteView):
    model = Chore
    success_url = reverse_lazy('chore-list')




#=============== PEOPLE ==================#
#=========================================#
class PeopleListView(LoginRequiredMixin, ListView):
    context_object_name = 'people'
    model = Person
    template_name = 'wac/people_list.html'

    def get_queryset(self):
        return Person.objects.filter(user=self.request.user).order_by('birthday', 'name')


class PersonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Person
    form_class = PersonEditForm
    template_name_suffix = '_create_form'

    def post(self, request, *args, **kwargs):
        form = PersonEditForm(request.POST, request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        new_person = form.save(commit=False)
        new_person.user = user
        new_person.mugshot = ''
        new_person.save()
        if form.cleaned_data['x'] is not None:
            image = form.crop_image()
            f= BytesIO()
            image.save(f, format='png')
            new_person.mugshot.save(new_person.name + '.png', ContentFile(f.getvalue()))
            f.close()

        new_person.save()

        chores = Chore.objects.filter(
            user = user
        )

        if user.welcomed:
            print("wac.views.PersonCreateView.form_valid: welcomed is True")
            messages.success(self.request, new_person.name + " was added successfully!")
            return HttpResponseRedirect(reverse('people-list'))
        else:
            print("wac.views.PersonCreateView.form_valid: welcomed is False")
            return HttpResponseRedirect(reverse('welcome-new2'))

    def form_invalid(self, form):
        pass


class PersonDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Person
    form_class = PersonEditForm

    def dispatch(self, request, *args, **kwargs):
        self.person = Person.objects.get(pk=self.kwargs['pk'])
        return super(PersonDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        form = PersonEditForm(instance=self.person,
                              initial={'name': self.person.name,
                                       'birthday': self.person.birthday,
                                       'phone_number': self.person.phone_number,
                                       'email': self.person.email,
                                       'day_off': self.person.day_off,
                                       'mugshot': self.person.mugshot})
        return render(request, 'wac/person_detail.html', {'form': form, 'person': self.person})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PersonEditForm(request.POST, request.FILES, instance=self.person)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        current_image = self.object.mugshot.name
        print("current_image = {}".format(current_image))
        self.object = form.save(commit=False)
        if form.cleaned_data['x'] is not None:
            image = form.crop_image()
            f= BytesIO()
            image.save(f, format='png')
            try:
                os.remove(settings.MEDIA_ROOT + current_image)
            except OSError:
                pass
            finally:
                self.object.mugshot.save(self.object.name + '.png', ContentFile(f.getvalue()))
                f.close()

        self.object.save()
        messages.success(self.request, self.object.name + " was updated successfully!")
        return HttpResponseRedirect(reverse('people-list'))

    def form_invalid(self, form):
        return render(self.request, 'wac/person_detail.html', {'form': form, 'person': self.person})


class PersonDelete(LoginRequiredMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('people-list')
