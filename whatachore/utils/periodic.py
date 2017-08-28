from useraccounts.models import User
from wac.models import Chore, Person, Week


def get_users():
    return User.objects.all()
