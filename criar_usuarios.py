#!/usr/bin/env python
"""
Script para criar usuários e grupos do sistema QualiSoja
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualisoja.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from analises.models import (
    AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado, 
    AnaliseUrase, AnaliseCinza, AnaliseTeorOleo, 
    AnaliseFibra, AnaliseFosforo
)

def criar_grupos_permissoes():
    """Criar grupos e suas permissões"""
    
    # Grupo Analista
    grupo_analista, created = Group.objects.get_or_create(name='Analista')
    if created:
        print("✓ Grupo 'Analista' criado")
    
    # Grupo Expedição
    grupo_expedicao, created = Group.objects.get_or_create(name='Expedição')
    if created:
        print("✓ Grupo 'Expedição' criado")
    
    # Permissões para Analista (todas as análises)
    modelos_analises = [
        AnaliseUmidade, AnaliseProteina, AnaliseOleoDegomado,
        AnaliseUrase, AnaliseCinza, AnaliseTeorOleo,
        AnaliseFibra, AnaliseFosforo
    ]
    
    for modelo in modelos_analises:
        content_type = ContentType.objects.get_for_model(modelo)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            grupo_analista.permissions.add(perm)
    
    # Permissões para Expedição (apenas visualização)
    for modelo in modelos_analises:
        content_type = ContentType.objects.get_for_model(modelo)
        view_permission = Permission.objects.filter(
            content_type=content_type, 
            codename__startswith='view_'
        )
        for perm in view_permission:
            grupo_expedicao.permissions.add(perm)
    
    print("✓ Permissões configuradas para os grupos")
    return grupo_analista, grupo_expedicao

def criar_usuarios():
    """Criar usuários do sistema"""
    
    # Criar grupos primeiro
    grupo_analista, grupo_expedicao = criar_grupos_permissoes()
    
    # Usuário Analista
    if not User.objects.filter(username='analista').exists():
        usuario_analista = User.objects.create_user(
            username='analista',
            email='analista@qualisoja.com',
            password='analista123',
            first_name='Analista',
            last_name='Sistema'
        )
        usuario_analista.groups.add(grupo_analista)
        print("✓ Usuário 'analista' criado - Senha: analista123")
    else:
        print("• Usuário 'analista' já existe")
    
    # Usuário Expedição
    if not User.objects.filter(username='expedicao').exists():
        usuario_expedicao = User.objects.create_user(
            username='expedicao',
            email='expedicao@qualisoja.com',
            password='expedicao123',
            first_name='Expedição',
            last_name='Sistema'
        )
        usuario_expedicao.groups.add(grupo_expedicao)
        print("✓ Usuário 'expedicao' criado - Senha: expedicao123")
    else:
        print("• Usuário 'expedicao' já existe")
    
    # Verificar se admin existe
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@qualisoja.com',
            password='admin'
        )
        print("✓ Superusuário 'admin' criado - Senha: admin")
    else:
        print("• Superusuário 'admin' já existe")

def main():
    """Função principal"""
    print("=== Configuração de Usuários QualiSoja ===")
    print()
    
    try:
        criar_usuarios()
        print()
        print("=== Usuários criados com sucesso! ===")
        print()
        print("Credenciais:")
        print("• Admin: admin / admin (Superusuário)")
        print("• Analista: analista / analista123 (Pode criar/editar análises)")
        print("• Expedição: expedicao / expedicao123 (Apenas visualização)")
        print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
