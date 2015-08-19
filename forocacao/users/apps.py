from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersAppConfig(AppConfig):
    name = 'forocacao.users'
    verbose_name = _('Users')
