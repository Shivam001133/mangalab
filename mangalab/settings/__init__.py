# local_settings.py
from split_settings.tools import include
from .components.base import INSTALLED_APPS

INSTALLED_APPS += (
  'raven.contrib.django.raven_compat',
)

include(
    'components/get_env.py',
    'components/base.py',
    'components/django_ckeditor.py',
    'components/celery.py',
)