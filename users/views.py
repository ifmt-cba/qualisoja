from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get('confirmPassword')
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
            profile.tipo_funcionario = tipo_funcionario
            profile.save()

            return redirect('/users/login')
        except Exception as e:
            print(f'Erro ao criar usuário: {e}')
            return redirect('/users/login')
        
def loginViews(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username')  # nome do input é "email", mas o valor é o username mesmo
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if not user:
            return redirect('users:login')

    auth.login(request, user)

    if user.is_superuser:
        return redirect('/admin/')

    try:
        profile = user.profile
        if profile.tipo_funcionario == 'analista':
            return redirect('analises:umidade_list')
        elif profile.tipo_funcionario == 'producao':
            return redirect('relatorios:gerar')
        else:
            return redirect('users:login')

    except ObjectDoesNotExist:
        print("Usuário sem profile! Criando agora...")
        Profile.objects.create(user=user)
        return redirect('users:login')
        

def logout(request):
    auth.logout(request)
    return redirect('users:login')