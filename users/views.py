from django.shortcuts import render, redirect
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

    elif request.method == "POST":
        username = request.POST.get('username')  # nome do input é "email", mas o valor é o username mesmo
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if not user:
            print("Erro: Usuário ou senha inválidos")
            return redirect('/users/login')

        auth.login(request, user)

        # Usuário autenticado! Agora redirecionar conforme tipo_funcionario
        if user.is_superuser:
            return redirect('/admin/')  # ou uma tela personalizada

        try:
            profile = user.profile
            if profile.tipo_funcionario == 'analista':
                return redirect('analises:umidade_list')  # ou dashboard analista
            elif profile.tipo_funcionario == 'produção':
                return redirect('relatorios:dashboard')  # ou o que quiser
            else:
                print("Erro: Tipo de funcionário desconhecido")
                return redirect('/users/login')
        except Profile.DoesNotExist:
            print("Erro: Perfil não encontrado")
            return redirect('/users/login')
        

