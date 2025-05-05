from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#def cadastrarAnalise(request):
#    return render(request, 'cadastrarAnalise.html')

# views.py
def cadastrarAnalise(request):
    contexto = {
        'intervalo': range(1, 9),  # Gera 1 até 8
    }
    return render(request, 'cadastrarAnalise.html', contexto)


def historicoAnalises(request):
    return render(request, 'historicoAnalises.html')


def relatorios(request):
    return render(request, 'relatorios.html')
