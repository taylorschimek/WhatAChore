from django.apps import AppConfig


class UseraccountsConfig(AppConfig):
    name = 'useraccounts'

    def ready(self):
        post_save.connect(week_post_save, weak=False, dispatch_uid="new_week")
