#!/usr/bin/env python
"""
Script principal de testes - Executa todos os testes do sistema
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from teste_analises import TesteAnalises
from teste_relatorios import TesteRelatorios

class TesteSistema:
    def __init__(self):
        self.inicio = datetime.now()
        print("=" * 60)
        print("    SISTEMA DE TESTES AUTOMATIZADOS - QUALISOJA")
        print("=" * 60)
        print(f"Iniciado em: {self.inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        print()
    
    def testar_conexao_banco(self):
        """Testa a conexão com o banco de dados"""
        print("--- Testando Conexão com Banco de Dados ---")
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                resultado = cursor.fetchone()
                if resultado and resultado[0] == 1:
                    print("✅ Conexão com banco de dados: OK")
                    return True
                else:
                    print("❌ Problema na conexão com banco de dados")
                    return False
        except Exception as e:
            print(f"❌ Erro na conexão com banco: {e}")
            return False
    
    def testar_modelos_django(self):
        """Testa se os modelos Django estão funcionando"""
        print("\n--- Testando Modelos Django ---")
        try:
            from analises.models import AnaliseUmidade
            from relatorios.models import RelatorioExpedicao
            from django.contrib.auth.models import User
            
            # Testar contagem de registros
            umidade_count = AnaliseUmidade.objects.count()
            relatorio_count = RelatorioExpedicao.objects.count()
            user_count = User.objects.count()
            
            print(f"✅ Análises de Umidade no banco: {umidade_count}")
            print(f"✅ Relatórios de Expedição no banco: {relatorio_count}")
            print(f"✅ Usuários no banco: {user_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro nos modelos Django: {e}")
            return False
    
    def executar_teste_analises(self):
        """Executa testes do módulo de análises"""
        print("\n" + "=" * 40)
        print("       MÓDULO DE ANÁLISES")
        print("=" * 40)
        
        try:
            teste_analises = TesteAnalises()
            resultado = teste_analises.executar_todos_testes()
            return resultado
        except Exception as e:
            print(f"❌ Erro crítico no teste de análises: {e}")
            return False
    
    def executar_teste_relatorios(self):
        """Executa testes do módulo de relatórios"""
        print("\n" + "=" * 40)
        print("       MÓDULO DE RELATÓRIOS")
        print("=" * 40)
        
        try:
            teste_relatorios = TesteRelatorios()
            resultado = teste_relatorios.executar_todos_testes()
            return resultado
        except Exception as e:
            print(f"❌ Erro crítico no teste de relatórios: {e}")
            return False
    
    def executar_testes_integracao(self):
        """Executa testes de integração entre módulos"""
        print("\n" + "=" * 40)
        print("       TESTES DE INTEGRAÇÃO")
        print("=" * 40)
        
        try:
            from analises.models import AnaliseUmidade
            from relatorios.models import RelatorioExpedicao
            from django.contrib.auth.models import User
            from decimal import Decimal
            from datetime import date, time
            
            # Criar usuário de teste
            usuario, _ = User.objects.get_or_create(
                username='integracao_teste',
                defaults={'email': 'integracao@teste.com'}
            )
            
            # Criar análise
            analise = AnaliseUmidade.objects.create(
                data=date.today(),
                usuario=usuario,
                horario=time(10, 0),
                tipo_amostra='FL',
                peso_amostra=Decimal('100.00'),
                resultado=Decimal('12.50')
            )
            print(f"✅ Análise criada: ID {analise.id}")
            
            # Criar relatório usando a análise
            relatorio = RelatorioExpedicao.objects.create(
                codigo='INT-TEST-001',
                cliente_nome_manual='Cliente Integração',
                data_inicial=date.today(),
                data_final=date.today(),
                tipo_analise='auto',
                parametros_incluidos=['umidade'],
                analises_selecionadas=[{
                    'id': analise.id,
                    'modelo': 'AnaliseUmidade',
                    'resultado': float(analise.resultado)
                }],
                usuario_responsavel=usuario
            )
            print(f"✅ Relatório criado: {relatorio.codigo}")
            
            # Verificar integração
            if len(relatorio.analises_selecionadas) > 0:
                analise_no_relatorio = relatorio.analises_selecionadas[0]
                if analise_no_relatorio['id'] == analise.id:
                    print("✅ Integração análise-relatório: OK")
                    resultado_integracao = True
                else:
                    print("❌ Problema na integração análise-relatório")
                    resultado_integracao = False
            else:
                print("❌ Nenhuma análise encontrada no relatório")
                resultado_integracao = False
            
            # Limpeza
            relatorio.delete()
            analise.delete()
            usuario.delete()
            print("✅ Dados de teste removidos")
            
            return resultado_integracao
            
        except Exception as e:
            print(f"❌ Erro no teste de integração: {e}")
            return False
    
    def gerar_relatorio_final(self, resultados):
        """Gera relatório final dos testes"""
        fim = datetime.now()
        duracao = fim - self.inicio
        
        print("\n" + "=" * 60)
        print("           RELATÓRIO FINAL DOS TESTES")
        print("=" * 60)
        
        print(f"Início: {self.inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Fim: {fim.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Duração: {duracao.total_seconds():.2f} segundos")
        print()
        
        total_testes = len(resultados)
        testes_passou = sum(resultados.values())
        testes_falhou = total_testes - testes_passou
        
        print("RESULTADOS POR MÓDULO:")
        for modulo, resultado in resultados.items():
            status = "✅ PASSOU" if resultado else "❌ FALHOU"
            print(f"  {modulo}: {status}")
        
        print(f"\nRESUMO GERAL:")
        print(f"  Total de módulos testados: {total_testes}")
        print(f"  Módulos que passaram: {testes_passou}")
        print(f"  Módulos que falharam: {testes_falhou}")
        print(f"  Taxa de sucesso: {(testes_passou/total_testes)*100:.1f}%")
        
        if all(resultados.values()):
            print("\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando corretamente.")
            return True
        else:
            print(f"\n⚠️  {testes_falhou} módulo(s) com falhas. Verifique os logs acima.")
            return False
    
    def executar_todos_testes(self):
        """Executa toda a suíte de testes"""
        resultados = {}
        
        # Testes básicos
        resultados['Conexão Banco'] = self.testar_conexao_banco()
        resultados['Modelos Django'] = self.testar_modelos_django()
        
        # Testes de módulos
        resultados['Módulo Análises'] = self.executar_teste_analises()
        resultados['Módulo Relatórios'] = self.executar_teste_relatorios()
        resultados['Integração'] = self.executar_testes_integracao()
        
        # Relatório final
        sucesso_geral = self.gerar_relatorio_final(resultados)
        
        return sucesso_geral

if __name__ == "__main__":
    print("Executando testes automatizados...")
    print("Pressione Ctrl+C para interromper")
    print()
    
    try:
        teste_sistema = TesteSistema()
        resultado = teste_sistema.executar_todos_testes()
        
        # Código de saída
        sys.exit(0 if resultado else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n❌ Erro crítico no sistema de testes: {e}")
        sys.exit(3)
