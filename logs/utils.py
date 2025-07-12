from django.contrib.contenttypes.models import ContentType
from .models import LogPersonalizado

def registrar_log(usuario, acao, obj=None):
    content_type = ContentType.objects.get_for_model(obj) if obj else None
    object_id = obj.pk if obj else None
    LogPersonalizado.objects.create(
        usuario=usuario,
        acao=acao,
        content_type=content_type,
        object_id=object_id
    )
