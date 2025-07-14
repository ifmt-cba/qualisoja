#!/usr/bin/env python
"""
Script para atualizar relatórios de expedição existentes com novos parâmetros obrigatórios.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import RelatorioExpedicao

def atualizar_relatorios():
    """Atualiza relatórios existentes com novos parâmetros obrigatórios."""
    
    print("🔄 Iniciando atualização de relatórios de expedição...")
    
    # Parâmetros obrigatórios atualizados
    parametros_obrigatorios = ['umidade', 'proteina', 'oleo']
    
    # Buscar todos os relatórios
    relatorios = RelatorioExpedicao.objects.all()
    
    print(f"📊 Encontrados {relatorios.count()} relatórios para atualizar")
    
    contador = 0
    for relatorio in relatorios:
        # Atualizar parâmetros obrigatórios
        relatorio.parametros_obrigatorios = parametros_obrigatorios
        
        # Garantir que todos os parâmetros obrigatórios estão incluídos
        parametros_incluidos = set(relatorio.parametros_incluidos or [])
        parametros_incluidos.update(parametros_obrigatorios)
        relatorio.parametros_incluidos = list(parametros_incluidos)
        
        # Salvar alterações
        relatorio.save()
        
        contador += 1
        print(f"✅ Relatório {relatorio.codigo} atualizado")
    
    print(f"🎉 Concluído! {contador} relatórios atualizados com sucesso.")
    print("📋 Parâmetros obrigatórios agora incluem: Umidade, Proteína e Óleo Degomado")

if __name__ == '__main__':
    atualizar_relatorios()
