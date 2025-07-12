from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    logger.info(f"Usuário '{user.username}' fez login.")

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    logger.info(f"Usuário '{user.username}' fez logout.")
