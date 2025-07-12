from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
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

            # Atribui grupo ao usuário
            grupo = Group.objects.get(name=tipo_funcionario)
            user.groups.add(grupo)

            return redirect('/users/login')
        except Exception as e:
            print(f'Erro ao criar usuário: {e}')
            return redirect('/users/login')


def loginViews(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('users:login')

        auth.login(request, user)

        # Registro de atividade de login
        try:
            from logs.models import LogPersonalizado
            grupos = ', '.join([g.name for g in user.groups.all()])
            acao = f'Usuário {user.username} (Grupo(s): {grupos}) acessou o sistema.'
            LogPersonalizado.objects.create(usuario=user, acao=acao)
        except Exception as e:
            print(f"Erro ao registrar log de login: {e}")

        if user.is_superuser:
            return redirect('/admin/')

        if user.groups.filter(name='Analista').exists():
            return redirect('analises:home')
        elif user.groups.filter(name='Produção').exists():
            return redirect('relatorios:gerar')
        else:
            messages.warning(request, "Usuário sem grupo definido.")
            return redirect('users:login')

def logout(request):
    auth.logout(request)
    return redirect('users:login')
