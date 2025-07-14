from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from logs.models import LogPersonalizado
from analises.models import AnaliseUmidade, AnaliseProteina  # ou outros
from django.contrib.auth.models import User

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    LogPersonalizado.objects.create(
        usuario=user,
        acao=f"{user.username} fez login no sistema."
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    LogPersonalizado.objects.create(
        usuario=user,
        acao=f"{user.username} fez logout do sistema."
    )

@receiver(post_save, sender=AnaliseUmidade)
def log_criacao_ou_edicao_umidade(sender, instance, created, **kwargs):
    acao = "criou" if created else "editou"
    LogPersonalizado.objects.create(
        usuario=instance.usuario_responsavel,  # ajuste conforme seu modelo
        acao=f"{instance.usuario_responsavel} {acao} uma Análise de Umidade (ID: {instance.id})"
    )

@receiver(post_delete, sender=AnaliseUmidade)
def log_exclusao_umidade(sender, instance, **kwargs):
    LogPersonalizado.objects.create(
        usuario=instance.usuario_responsavel,
        acao=f"{instance.usuario_responsavel} excluiu uma Análise de Umidade (ID: {instance.id})"
    )
