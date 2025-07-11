from analises.models import AnaliseFibra
from decimal import Decimal
from datetime import date, time

# Criar dados de teste para análise de fibra
teste1 = AnaliseFibra.objects.create(
    data=date.today(),
    horario=time(14, 30),
    tipo_amostra='FL',
    peso_amostra=Decimal('2.0000'),
    peso_tara=Decimal('1.5000'),
    peso_fibra=Decimal('0.8000'),
    peso_branco=Decimal('0.2000')
)

teste2 = AnaliseFibra.objects.create(
    data=date.today(),
    horario=time(15, 45),
    tipo_amostra='SI',
    peso_amostra=Decimal('1.8000'),
    peso_tara=Decimal('1.2000'),
    peso_fibra=Decimal('0.6000'),
    peso_branco=Decimal('0.1000')
)

print(f"Criados {AnaliseFibra.objects.count()} registros de teste")
for analise in AnaliseFibra.objects.all():
    print(f"- {analise} - Resultado: {analise.resultado}%")
