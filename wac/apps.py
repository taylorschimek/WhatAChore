from django.apps import AppConfig


class WacConfig(AppConfig):
    name = 'wac'

    def ready(self):
        import wac.signals.handlers  #noqa
