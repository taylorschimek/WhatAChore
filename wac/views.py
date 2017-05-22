import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, DeleteView
from django.views.generic.edit import FormMixin

from wac.models import Chore, Person, Week

from .forms import ChoreEditForm, PersonEditForm




#=============== LINEUP ==================#
#=========================================#
def lineup(request):
    new_week = Week.objects.create()
    return render(request, 'wac/lineup_layout.html')




#=============== CHORES ==================#
#=========================================#

class ChoreListView(LoginRequiredMixin, ListView):
    context_object_name = 'chores'
    model = Chore

    def get_queryset(self):
        return Chore.objects.filter(user=self.request.user)


class ChoreCreateView(SuccessMessageMixin, CreateView):
    model = Chore
    # success_url = '/success/'
    # success_message = "%(name)s was created successfully"
    # fields = '__all__'
    form_class = ChoreEditForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, self.object.task + " was added successfully!")
        return HttpResponseRedirect(reverse('chore-list'))

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         task=self.object.task,
    #     )


class ChoreDetailView(FormMixin, DetailView):
    model = Chore
    form_class = ChoreEditForm

    def dispatch(self, request, *args, **kwargs):
        print('dispatch')
        self.chore = Chore.objects.get(pk=self.kwargs['pk'])
        return super(ChoreDetailView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        print('get_context_data')
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        print('get')
        form = ChoreEditForm(instance=self.chore,
                             initial={'task': self.chore.task,
                                      'duration': self.chore.duration,
                                      'description': self.chore.description,
                                      'interval': self.chore.interval,
                                      'sub_interval': self.chore.sub_interval,
                                      'age_restriction': self.chore.age_restriction,
                                      'last_assigned': self.chore.last_assigned,
                                      'chore_icon_location': self.chore.chore_icon_location})
        return render(request, 'wac/chore_detail.html', {'form': form, 'chore': self.chore, 'gobble': "Create New Chore"})

    def post(self, request, *args, **kwargs):
        print('post')
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()
        form = ChoreEditForm(request.POST, instance=self.chore)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print('valid')
        form.save()
        messages.success(self.request, self.object.task + " was updated successfully!")
        return HttpResponseRedirect(reverse('chore-list'))

    def form_invalid(self, form):
        print('invalid')
        return render(self.request, 'wac/chore_detail.html', {'form': form, 'chore': self.chore})


class ChoreDelete(DeleteView):
    model = Chore
    success_url = reverse_lazy('chore-list')




#=============== PEOPLE ==================#
#=========================================#
class PeopleListView(LoginRequiredMixin, ListView):
    context_object_name = 'people'
    model = Person
    template_name = 'wac/people_list.html'

    def get_queryset(self):
        return Person.objects.filter(user=self.request.user)


class PersonCreateView(SuccessMessageMixin, CreateView):
    model = Person
    # success_url = '/success/'
    # success_message = "%(name)s was created successfully"
    form_class = PersonEditForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        for object in self.request.FILES:
            print(object)
        self.object.mugshot = ""
        self.object.save()
        self.object.mugshot = self.request.FILES['mugshot']
        self.object.save()
        messages.success(self.request, self.object.name + " was added successfully!")
        return HttpResponseRedirect(reverse('people-list'))




class PersonDetailView(FormMixin, DetailView):
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
        form.save()
        messages.success(self.request, self.object.name + " was updated successfully!")
        return HttpResponseRedirect(reverse('people-list'))

    def form_invalid(self, form):
        return render(self.request, 'wac/person_detail.html', {'form': form, 'person': self.person})


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy('people-list')
