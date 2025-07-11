from analises.models import AnaliseTeorOleo

print("=== ANALISES DE TEOR DE OLEO ===")
analises = AnaliseTeorOleo.objects.all()
print(f"Total: {analises.count()}")

for a in analises:
    print(f"- ID: {a.pk}, Data: {a.data}, Teor: {a.teor_oleo}%")
