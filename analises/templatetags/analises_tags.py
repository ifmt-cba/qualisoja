from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def safe_resultado(analise):
    """Retorna o resultado formatado de forma segura"""
    try:
        if analise and hasattr(analise, 'get_resultado_formatado'):
            return analise.get_resultado_formatado()
        return "0"
    except (InvalidOperation, ValueError, AttributeError):
        return "0"

@register.filter
def safe_decimal(value):
    """Converte valor para Decimal de forma segura"""
    try:
        if value is None:
            return Decimal('0')
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0')

@register.filter
def safe_compare(resultado, valor):
    """Compara valores de forma segura"""
    try:
        if resultado is None:
            return False
        resultado_decimal = Decimal(str(resultado))
        valor_decimal = Decimal(str(valor))
        return resultado_decimal >= valor_decimal
    except (InvalidOperation, ValueError, TypeError):
        return False
