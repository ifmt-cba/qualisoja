from django.shortcuts import render

def home(request):
    """View para a página inicial completa do QualiSoja"""
    return render(request, 'home.html')

def home_simple(request):
    """View para a página inicial simples/dashboard do QualiSoja"""
    return render(request, 'home_simple.html')
