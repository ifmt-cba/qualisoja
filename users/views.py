from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get('confirmPassword')
        telefone = request.POST.get('phone')
        cpf = request.POST.get('cpf')
        tipo_funcionario = request.POST.get('tipo_funcionario')

        if User.objects.filter(username=username).exists():
            print('Erro: Usuário já existe')
            return redirect('/users/cadastro')

        if password != confirmPassword:
            print('Erro: Senhas não coincidem')
            return redirect('/users/cadastro')

        if len(password) < 6:
            print('Erro: Senha muito curta')
            return redirect('/users/cadastro')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile.objects.get(user=user)
            profile.telefone = telefone
            profile.cpf = cpf
            profile.tipo_funcionario = tipo_funcionario
            profile.save()

            return redirect('/users/login')
        except Exception as e:
            print(f'Erro ao criar usuário: {e}')
            return redirect('/users/login')
        
def loginViews(request):
    if request.method == "GET":
        return render(request, 'login.html')
