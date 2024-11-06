from harvest_routes.models import Harvester
from src.message import logging_message
from django.db import models
import logging


logger = logging.getLogger(__name__)


def get_domain_info(domain_name: str) -> models:
    domain = "" if domain_name is None else domain_name.strip()
    if domain_name:
        try:
            domain = Harvester.objects.get(domain_name=domain_name, is_active=True)
        except Harvester.DoesNotExist:
            logger.exception(
                logging_message.MODELS_NOT_FOUND.format(MESSAGE=domain_name)
            )
    return domain
