
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get('confirmPassword')
        tipo_funcionario = request.POST.get('tipo_funcionario')

        # Validação de email corporativo
        if not email or not email.endswith("@colaborador.qualisoja.com.br"):
            messages.error(request, "Utilize um email corporativo (@colaborador.qualisoja.com.br)")
            return redirect('/users/cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('/users/cadastro')

        if password != confirmPassword:
            messages.error(request, 'Senhas não coincidem')
            return redirect('/users/cadastro')

        if len(password) < 6:
            messages.error(request, 'Senha muito curta')
            return redirect('/users/cadastro')

        try:
            # Usa o email como username
            user = User.objects.create_user(username=email, email=email, password=password)
            grupo = Group.objects.get(name=tipo_funcionario)
            user.groups.add(grupo)
            return redirect('/users/login')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {e}')
            return redirect('/users/login')


def loginViews(request):  # Login deve ser público
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":

        username_or_email = request.POST.get('username')  # Campo vem como 'username' do template
        password = request.POST.get('password')

        # Tentar autenticação por username primeiro
        user = auth.authenticate(request, username=username_or_email, password=password)
        
        # Se não funcionar, tentar por email (usando filter para evitar múltiplos resultados)
        if not user:
            try:
                user_obj = User.objects.filter(email=username_or_email).first()
                if user_obj:
                    user = auth.authenticate(request, username=user_obj.username, password=password)
            except Exception:
                user = None

        if not user:
            messages.error(request, "Usuário/email ou senha inválidos.")
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

@login_required
def logout(request):
    auth.logout(request)
    return redirect('users:login')
