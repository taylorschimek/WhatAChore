from django.apps import AppConfig


class UseraccountsConfig(AppConfig):
    name = 'useraccounts'

    def ready(self):
        # import wac.signals
        post_save.connect(week_post_save, weak=False, dispatch_uid="new_week")
