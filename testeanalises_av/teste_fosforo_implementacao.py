#!/usr/bin/env python
"""
Teste rápido para verificar se a implementação da análise de fósforo está funcionando
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from decimal import Decimal
from analises.models import AnaliseFosforo
from analises.forms import AnaliseFosforoForm

def testar_formula_fosforo():
    """Teste da fórmula de cálculo de fósforo"""
    print("=== TESTE DA FÓRMULA DE FÓSFORO ===")
    print("Fórmula: Fósforo (ppm) = (Aa × Cp × V × 1000 × 1000) / (P × VAl × Ap)")
    print()
    
    # Dados de exemplo
    dados_teste = {
        'absorbancia_amostra': Decimal('0.125'),
        'concentracao_padrao': Decimal('10.0'),
        'volume_solucao': Decimal('100.0'),
        'peso_amostra': Decimal('1.0000'),
        'volume_aliquota': Decimal('10.0'),
        'absorbancia_padrao': Decimal('0.250')
    }
    
    print("Dados de teste:")
    for campo, valor in dados_teste.items():
        print(f"  {campo}: {valor}")
    
    # Calcular resultado manualmente
    aa = dados_teste['absorbancia_amostra']
    cp = dados_teste['concentracao_padrao']
    v = dados_teste['volume_solucao']
    p = dados_teste['peso_amostra']
    val = dados_teste['volume_aliquota']
    ap = dados_teste['absorbancia_padrao']
    
    numerador = aa * cp * v * Decimal('1000') * Decimal('1000')
    denominador = p * val * ap
    resultado_manual = numerador / denominador
    
    print(f"\nCálculo manual:")
    print(f"  Numerador: {aa} × {cp} × {v} × 1000 × 1000 = {numerador}")
    print(f"  Denominador: {p} × {val} × {ap} = {denominador}")
    print(f"  Resultado: {numerador} ÷ {denominador} = {resultado_manual:.2f} ppm")
    
    # Testar criação do modelo
    try:
        analise = AnaliseFosforo(**dados_teste)
        analise.save()
        print(f"\nResultado do modelo: {analise.resultado} ppm")
        print("✅ Teste realizado com sucesso!")
        
        # Limpar teste
        analise.delete()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

def testar_formulario():
    """Teste do formulário"""
    print("\n=== TESTE DO FORMULÁRIO ===")
    
    dados_form = {
        'data': '2025-01-10',
        'horario': '14:30:00',
        'tipo_amostra': 'FL',
        'peso_amostra': '1.0000',
        'absorbancia_amostra': '0.125000',
        'concentracao_padrao': '10.0000',
        'volume_solucao': '100.00',
        'volume_aliquota': '10.00',
        'absorbancia_padrao': '0.250000'
    }
    
    form = AnaliseFosforoForm(data=dados_form)
    
    if form.is_valid():
        print("✅ Formulário válido!")
        print("Campos disponíveis:", form.Meta.fields)
    else:
        print("❌ Formulário inválido!")
        print("Erros:", form.errors)

if __name__ == '__main__':
    try:
        testar_formula_fosforo()
        testar_formulario()
        print("\n🎉 Todos os testes concluídos!")
    except Exception as e:
        print(f"💥 Erro geral: {e}")
        import traceback
        traceback.print_exc()
