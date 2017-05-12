from django.views.generic import FormView
from useraccounts.forms import RegistrationForm

#===============
#=========================================#
class LandingView(FormView):
    template_name = 'landing.html'
    form_class = RegistrationForm
