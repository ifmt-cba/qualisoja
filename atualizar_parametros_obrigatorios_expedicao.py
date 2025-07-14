#!/usr/bin/env python
"""
Script para atualizar os parâmetros obrigatórios dos relatórios de expedição
baseado no tipo de análise (óleo ou farelo) conforme especificado na imagem.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from relatorios.models import RelatorioExpedicao

def determinar_tipo_analise(relatorio):
    """
    Determina o tipo de análise baseado nos lotes do relatório.
    Retorna 'farelo' se algum lote for de farelo, senão 'oleo'.
    """
    for lote in relatorio.lotes.all():
        # Verificar se é lote de farelo baseado no código ou observações
        if ('farelo' in lote.codigo.lower() or 
            (lote.observacoes and 'farelo' in lote.observacoes.lower())):
            return 'farelo'
    return 'oleo'

def get_parametros_obrigatorios_por_tipo(tipo_analise):
    """Retorna os parâmetros obrigatórios baseados no tipo de análise."""
    if tipo_analise == 'farelo':
        # AnaliseFarelo: umidade, proteína, teorÓleo
        return ['umidade', 'proteina', 'teor_oleo']
    else:
        # AnaliseOleo: umidade, acidez, índiceSabão, sílica, fósforo, urase
        return ['umidade', 'acidez', 'indice_sabao', 'silica', 'fosforo', 'urase']

def main():
    print("🔄 Atualizando parâmetros obrigatórios dos relatórios de expedição...")
    
    # Buscar todos os relatórios de expedição
    relatorios = RelatorioExpedicao.objects.all()
    
    total_relatorios = relatorios.count()
    print(f"📊 Encontrados {total_relatorios} relatórios de expedição")
    
    if total_relatorios == 0:
        print("ℹ️ Nenhum relatório de expedição encontrado.")
        return
    
    atualizados = 0
    
    for relatorio in relatorios:
        try:
            # Determinar tipo de análise baseado nos lotes
            tipo_analise = determinar_tipo_analise(relatorio)
            parametros_obrigatorios = get_parametros_obrigatorios_por_tipo(tipo_analise)
            
            # Atualizar parâmetros obrigatórios
            relatorio.parametros_obrigatorios = parametros_obrigatorios
            
            # Combinar parâmetros obrigatórios com incluídos
            parametros_incluidos = relatorio.parametros_incluidos or []
            parametros_completos = list(set(parametros_obrigatorios + parametros_incluidos))
            relatorio.parametros_incluidos = parametros_completos
            
            relatorio.save()
            
            print(f"✅ Relatório {relatorio.codigo}: {tipo_analise} -> {parametros_obrigatorios}")
            atualizados += 1
            
        except Exception as e:
            print(f"❌ Erro ao atualizar relatório {relatorio.codigo}: {str(e)}")
            continue
    
    print(f"\n🎉 Atualização concluída!")
    print(f"📈 Total de relatórios atualizados: {atualizados}/{total_relatorios}")
    
    if atualizados > 0:
        print("\n📋 Parâmetros obrigatórios por tipo:")
        print("🛢️  AnaliseOleo: umidade, acidez, índice_sabao, silica, fosforo, urase")
        print("🌾 AnaliseFarelo: umidade, proteina, teor_oleo")

if __name__ == "__main__":
    main()
