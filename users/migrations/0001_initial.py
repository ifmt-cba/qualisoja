# Generated by Django 5.2.1 on 2025-07-07 20:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('tipo_funcionario', models.CharField(blank=True, choices=[('analista', 'Analista'), ('producao', 'Produção'), ('classificacao-producao', 'Classificação - Produção')], max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
