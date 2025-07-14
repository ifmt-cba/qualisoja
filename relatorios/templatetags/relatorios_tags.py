from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Template filter para acessar itens de dicionário usando chave.
    Uso: {{ meu_dict|get_item:chave }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def get_nested_item(dictionary, keys):
    """
    Template filter para acessar itens de dicionário aninhado.
    Uso: {{ meu_dict|get_nested_item:"chave1,chave2" }}
    """
    if dictionary is None:
        return None
    
    if isinstance(keys, str):
        keys = keys.split(',')
    
    current = dictionary
    for key in keys:
        if current is None or not isinstance(current, dict):
            return None
        current = current.get(key.strip())
    
    return current


@register.simple_tag
def get_analise_valor(dados_analises, lote_codigo, parametro):
    """
    Template tag para obter valor de análise específica.
    Uso: {% get_analise_valor dados_analises lote.codigo parametro %}
    """
    if not dados_analises or lote_codigo not in dados_analises:
        return None
    
    lote_dados = dados_analises[lote_codigo]
    return lote_dados.get(parametro)
