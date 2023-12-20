from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import logging
from utils import envs


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Command(BaseCommand):
    """
    a class for custom command execution in manage.py
    """

    help = "create superuser"

    def handle(self, *args, **options):
        """
        handler
        """
        try:
            User = get_user_model()  # noqa
            User.objects.create_superuser(
                envs.SCRIPT_USER,
                envs.SCRIPT_USER_EMAIL,
                envs.SCRIPT_PASSWORD,
            )
            logging.info("Superuser created...")
        except Exception as err:
            logging.info("Account maybe existing already..")
            logging.error(err)
