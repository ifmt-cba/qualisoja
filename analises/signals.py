import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado

logger = logging.getLogger(__name__)

@receiver(post_save, sender=AnaliseUmidade)
def log_umidade_save(sender, instance, created, **kwargs):
    action = "criada" if created else "atualizada"
    logger.info(f"Análise de Umidade {action} por {instance.usuario_responsavel.username} (ID: {instance.id})")

@receiver(post_delete, sender=AnaliseUmidade)
def log_umidade_delete(sender, instance, **kwargs):
    logger.warning(f"Análise de Umidade DELETADA (ID: {instance.id})")

# Repita para os outros modelos
