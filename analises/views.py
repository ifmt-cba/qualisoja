from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def cadastrarAnalise(request):
    return render(request, 'cadastrarAnalise.html')