#!/usr/bin/env python
"""
Teste da lista de fósforo com as novas alterações
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

def testar_lista_fosforo():
    """Criar dados de teste e verificar a formatação na lista"""
    print("=== TESTE DA LISTA DE FÓSFORO ===")
    print("Criando dados de teste com diferentes configurações...")
    print()
    
    # Dados de teste com diferentes casas decimais
    dados_teste = [
        {
            'absorbancia': Decimal('0.000015'),  # ~60 ppm (ÓTIMO)
            'casas': 0,
            'descricao': 'Resultado ÓTIMO - número inteiro'
        },
        {
            'absorbancia': Decimal('0.000025'),  # ~100 ppm (BOM)
            'casas': 0,
            'descricao': 'Resultado BOM - número inteiro'
        },
        {
            'absorbancia': Decimal('0.000050'),  # ~200 ppm (RUIM)
            'casas': 0,
            'descricao': 'Resultado RUIM - número inteiro'
        },
        {
            'absorbancia': Decimal('0.000030'),  # ~120 ppm (BOM)
            'casas': 2,
            'descricao': 'Resultado BOM - 2 casas decimais'
        }
    ]
    
    analises_criadas = []
    
    try:
        # Criar análises de teste
        for i, dados in enumerate(dados_teste):
            analise = AnaliseFosforo(
                absorbancia_amostra=dados['absorbancia'],
                casas_decimais=dados['casas'],
                tipo_amostra='FL'
            )
            analise.save()
            analises_criadas.append(analise)
            
            print(f"✅ Análise {i+1} criada:")
            print(f"   Absorbância: {dados['absorbancia']}")
            print(f"   Resultado: {analise.resultado} ppm")
            print(f"   Formatado: {analise.get_resultado_formatado()} ppm")
            print(f"   Casas decimais: {analise.casas_decimais}")
            print(f"   Descrição: {dados['descricao']}")
            print()
        
        print("📋 RESUMO PARA LISTA:")
        print("| ID | Resultado | Formatado | Casas | Avaliação |")
        print("|----|-----------|-----------|-------|-----------|")
        
        for analise in analises_criadas:
            resultado = float(analise.resultado)
            if resultado < 80:
                avaliacao = "ÓTIMO"
            elif 80 <= resultado <= 180:
                avaliacao = "BOM"
            else:
                avaliacao = "RUIM"
            
            print(f"| {analise.id:2d} | {analise.resultado:>8} | {analise.get_resultado_formatado():>9} | {analise.casas_decimais:>5} | {avaliacao:>9} |")
        
        print()
        print("🎯 VERIFICAÇÃO DA LISTA:")
        print("- A lista deve usar get_resultado_formatado() para exibir os valores")
        print("- Números inteiros não devem ter casas decimais desnecessárias") 
        print("- A avaliação (ÓTIMO/BOM/RUIM) deve funcionar corretamente")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpar dados de teste
        print("\n🧹 Limpando dados de teste...")
        for analise in analises_criadas:
            try:
                analise.delete()
                print(f"   Análise {analise.id} removida")
            except:
                pass

def verificar_metodo_formatacao():
    """Verificar se o método get_resultado_formatado está funcionando"""
    print("\n=== TESTE DO MÉTODO DE FORMATAÇÃO ===")
    
    testes = [
        (100.0, 0, "100"),
        (100.0, 1, "100.0"),
        (100.0, 2, "100.00"),
        (99.5, 0, "100"),  # Arredondamento
        (99.5, 1, "99.5"),
    ]
    
    for valor, casas, esperado in testes:
        try:
            analise = AnaliseFosforo(
                absorbancia_amostra=Decimal('0.000025'),
                casas_decimais=casas
            )
            analise.resultado = Decimal(str(valor))
            analise.casas_decimais = casas
            
            resultado = analise.get_resultado_formatado()
            status = "✅" if resultado == esperado else "❌"
            
            print(f"{status} Valor: {valor} | Casas: {casas} | Esperado: '{esperado}' | Obtido: '{resultado}'")
            
        except Exception as e:
            print(f"❌ Erro no teste {valor}, {casas}: {e}")

if __name__ == '__main__':
    try:
        testar_lista_fosforo()
        verificar_metodo_formatacao()
        print("\n🎉 Testes da lista concluídos!")
        
    except Exception as e:
        print(f"💥 Erro geral: {e}")
        import traceback
        traceback.print_exc()
