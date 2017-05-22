
from django.conf import settings
from django.views.generic import DetailView, FormView, TemplateView
from useraccounts.forms import RegistrationForm
from wac.views import PersonDetailView
from wac.models import Person

#===============
#=========================================#
class LandingView(FormView):
    template_name = 'landing.html'
    form_class = RegistrationForm
