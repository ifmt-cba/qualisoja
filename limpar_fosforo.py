#!/usr/bin/env python
"""
Script para limpar dados problemáticos de análises de fósforo
"""
import os
import sys
import django

# Configurar Django
sys.path.append('c:/Users/rodri/qualisoja')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from analises.models import AnaliseFosforo
from decimal import Decimal, InvalidOperation

def limpar_dados_problematicos():
    """Limpar registros com dados inválidos"""
    print("=== LIMPEZA DE DADOS PROBLEMÁTICOS ===")
    print("Verificando registros de análises de fósforo...")
    
    registros_removidos = 0
    registros_corrigidos = 0
    
    try:
        # Buscar todos os registros
        analises = AnaliseFosforo.objects.all()
        print(f"Total de registros encontrados: {analises.count()}")
        
        for analise in analises:
            try:
                # Tentar acessar todos os campos para verificar se há problemas
                _ = str(analise.resultado)
                _ = str(analise.absorbancia_amostra)
                _ = str(analise.peso_amostra)
                _ = str(analise.concentracao_padrao)
                _ = str(analise.volume_solucao)
                _ = str(analise.volume_aliquota)
                _ = str(analise.absorbancia_padrao)
                
                # Verificar se casas_decimais existe e é válido
                if not hasattr(analise, 'casas_decimais') or analise.casas_decimais is None:
                    print(f"Corrigindo casas_decimais para análise ID {analise.id}")
                    analise.casas_decimais = 0
                    analise.save()
                    registros_corrigidos += 1
                
                # Tentar formatar o resultado
                _ = analise.get_resultado_formatado()
                
                print(f"✅ Registro ID {analise.id} está OK")
                
            except (InvalidOperation, ValueError, AttributeError) as e:
                print(f"❌ Problema com registro ID {analise.id}: {e}")
                print(f"   Removendo registro problemático...")
                analise.delete()
                registros_removidos += 1
                
            except Exception as e:
                print(f"⚠️  Erro inesperado com registro ID {analise.id}: {e}")
                # Tentar remover também
                try:
                    analise.delete()
                    registros_removidos += 1
                except:
                    print(f"   Não foi possível remover o registro")
    
    except Exception as e:
        print(f"❌ Erro ao acessar registros: {e}")
        print("Tentando limpar toda a tabela...")
        try:
            AnaliseFosforo.objects.all().delete()
            print("✅ Tabela limpa completamente")
            registros_removidos = "todos"
        except Exception as cleanup_error:
            print(f"❌ Erro ao limpar tabela: {cleanup_error}")
    
    print(f"\n📊 RESUMO:")
    print(f"- Registros removidos: {registros_removidos}")
    print(f"- Registros corrigidos: {registros_corrigidos}")
    print(f"- Total de registros restantes: {AnaliseFosforo.objects.count()}")

def criar_registro_teste():
    """Criar um registro de teste válido"""
    print("\n=== CRIANDO REGISTRO DE TESTE ===")
    
    try:
        analise = AnaliseFosforo(
            absorbancia_amostra=Decimal('0.000025'),
            peso_amostra=Decimal('1.0000'),
            concentracao_padrao=Decimal('10.0000'),
            volume_solucao=Decimal('100.00'),
            volume_aliquota=Decimal('10.00'),
            absorbancia_padrao=Decimal('0.250000'),
            casas_decimais=0,
            tipo_amostra='FL'
        )
        analise.save()
        
        print(f"✅ Registro de teste criado com ID: {analise.id}")
        print(f"   Resultado: {analise.resultado} ppm")
        print(f"   Formatado: {analise.get_resultado_formatado()} ppm")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar registro de teste: {e}")
        return False

if __name__ == '__main__':
    try:
        limpar_dados_problematicos()
        if AnaliseFosforo.objects.count() == 0:
            criar_registro_teste()
        print("\n🎉 Limpeza concluída! Agora tente acessar a lista novamente.")
        
    except Exception as e:
        print(f"💥 Erro geral: {e}")
        import traceback
        traceback.print_exc()
