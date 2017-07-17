from useraccounts.models import User
from wac.models import Chore, Person, Week


def get_no_of_users():
    users = User.objects.all()
    return len(users)

def get_users():
    return User.objects.all()

# This worked, but might be too singularly large.....
# def trial_create_assignments():
#     users = User.objects.all()
#     for user in users:
#         # if len(Person.objects.filter(user=user)) and len(Chore.objects.filter(user=user)):
#         try:
#             new_week = Week.create(current_user=user)
#
#         except ZeroDivisionError:


# def user_assignments(user):
#     print("user_assignment called for {}".format(user))
#     try:
#         new_week = Week.create(current_user=user)
#         print("Try succeeded")
#         # email user assignments?
#     except ZeroDivisionError:
#         print("Try failed")
#         # email user that they're missing either workers or chores and assignments cannot be made.
