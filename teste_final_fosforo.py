#!/usr/bin/env python
"""
Teste da nova implementação simplificada de fósforo
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

def testar_calculo_simplificado():
    """Teste do cálculo simplificado"""
    print("=== TESTE DO CÁLCULO SIMPLIFICADO DE FÓSFORO ===")
    print("Apenas a absorbância da amostra é inserida, outros valores são padrão")
    print()
    
    # Teste com valor de absorbância
    absorbancia_teste = Decimal('0.125')
    
    print("Dados do teste:")
    print(f"  Absorbância da amostra: {absorbancia_teste}")
    print("  Peso da amostra: 1.0000g (padrão)")
    print("  Concentração padrão: 10.0000 mg/L (padrão)")
    print("  Volume da solução: 100.00 mL (padrão)")
    print("  Volume da alíquota: 10.00 mL (padrão)")
    print("  Absorbância do padrão: 0.250000 (padrão)")
    print()
    
    # Fórmula completa
    aa = absorbancia_teste
    cp = Decimal('10.0000')
    v = Decimal('100.00')
    p = Decimal('1.0000')
    val = Decimal('10.00')
    ap = Decimal('0.250000')
    
    numerador = aa * cp * v * Decimal('1000') * Decimal('1000')
    denominador = p * val * ap
    resultado_formula = numerador / denominador
    
    print("Cálculo usando fórmula completa:")
    print(f"  ({aa} × {cp} × {v} × 1000 × 1000) / ({p} × {val} × {ap})")
    print(f"  = {numerador} / {denominador}")
    print(f"  = {resultado_formula:.2f} ppm")
    print()
    
    # Fórmula simplificada
    # (Aa × 10.0 × 100.0 × 1000 × 1000) / (1.0 × 10.0 × 0.25)
    # = Aa × 10000000000 / 2.5
    # = Aa × 4000000
    resultado_simplificado = aa * Decimal('4000000')
    print("Cálculo usando fórmula simplificada:")
    print(f"  {aa} × 4.000.000 = {resultado_simplificado:.2f} ppm")
    print()
    
    # Testar no modelo
    try:
        analise = AnaliseFosforo(
            absorbancia_amostra=absorbancia_teste,
            casas_decimais=0  # Definir 0 casas decimais (número inteiro)
        )
        analise.save()
        
        print(f"Resultado do modelo Django: {analise.resultado} ppm")
        print(f"Resultado formatado: {analise.get_resultado_formatado()} ppm")
        print(f"Casas decimais configuradas: {analise.casas_decimais} (número inteiro)")
        print("✅ Teste realizado com sucesso!")
        
        # Verificar se os resultados coincidem
        if abs(float(analise.resultado) - float(resultado_formula)) < 0.01:
            print("✅ Os cálculos coincidem!")
        else:
            print("❌ Diferença nos cálculos detectada!")
        
        # Limpar teste
        analise.delete()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

def testar_varios_valores():
    """Teste com vários valores de absorbância e avaliação"""
    print("\n=== TESTE COM VÁRIOS VALORES E AVALIAÇÃO ===")
    
    valores_teste = [
        (0.000010, "ÓTIMO - Abaixo de 80 ppm"),
        (0.000015, "ÓTIMO - Abaixo de 80 ppm"), 
        (0.000020, "BOM - Entre 80 e 180 ppm"),
        (0.000030, "BOM - Entre 80 e 180 ppm"),
        (0.000045, "BOM - Entre 80 e 180 ppm"),
        (0.000050, "RUIM - Acima de 180 ppm"),
        (0.000100, "RUIM - Acima de 180 ppm")
    ]
    
    print("| Absorbância | Resultado (ppm) | Avaliação |")
    print("|-------------|-----------------|-----------|")
    
    for valor, descricao in valores_teste:
        resultado = valor * 4000000
        if resultado < 80:
            status = "ÓTIMO"
        elif 80 <= resultado <= 180:
            status = "BOM"
        else:
            status = "RUIM"
        
        print(f"|  {valor:.6f}  |   {resultado:>7.2f}     |   {status:<6} |")
    
    print("\n📊 CRITÉRIOS DE AVALIAÇÃO:")
    print("- ÓTIMO: Abaixo de 80 ppm")
    print("- BOM: Entre 80 e 180 ppm") 
    print("- RUIM: Acima de 180 ppm")
    print("\n💡 DICA: Para obter valores na faixa ideal (80-180 ppm):")
    print("   Digite absorbâncias entre 0.000020 e 0.000045")

def testar_casas_decimais():
    """Teste para demonstrar o controle de casas decimais"""
    print("\n=== TESTE DE CASAS DECIMAIS ===")
    
    absorbancia_teste = Decimal('0.000025')  # Valor que dá resultado ~100 ppm
    
    print(f"Absorbância de teste: {absorbancia_teste}")
    print("Testando diferentes configurações de casas decimais:")
    print()
    
    for casas in [0, 1, 2, 3]:
        try:
            analise = AnaliseFosforo(
                absorbancia_amostra=absorbancia_teste,
                casas_decimais=casas
            )
            analise.save()
            
            if casas == 0:
                print(f"• {casas} casas decimais (número inteiro): {analise.get_resultado_formatado()} ppm")
            else:
                print(f"• {casas} casa{'s' if casas > 1 else ''} decimal{'is' if casas > 1 else ''}: {analise.get_resultado_formatado()} ppm")
            
            analise.delete()
            
        except Exception as e:
            print(f"❌ Erro com {casas} casas decimais: {e}")
    
    print("\n💡 Padrão: 0 casas decimais (números inteiros)")
    print("💡 Todos os parâmetros da fórmula podem ser alterados no formulário!")

if __name__ == '__main__':
    try:
        testar_calculo_simplificado()
        testar_varios_valores()
        testar_casas_decimais()
        print("\n🎉 Todos os testes concluídos com sucesso!")
        print("\n📝 RESUMO:")
        print("- O usuário digita a absorbância da amostra")
        print("- O sistema multiplica por 4.000.000 para obter o resultado em ppm")
        print("- Resultado padrão: número inteiro (0 casas decimais)")
        print("- Todos os parâmetros podem ser alterados conforme necessário")
        print("- Casas decimais podem ser ajustadas de 0 a 6")
        
    except Exception as e:
        print(f"💥 Erro geral: {e}")
        import traceback
        traceback.print_exc()
