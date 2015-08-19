from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EventAppConfig(AppConfig):
    name = 'forocacao.app'
    verbose_name = _('Event Management')
