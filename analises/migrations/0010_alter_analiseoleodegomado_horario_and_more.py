# Generated by Django 5.2.3 on 2025-06-19 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analises', '0009_alter_analiseoleodegomado_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analiseoleodegomado',
            name='horario',
            field=models.TimeField(default=datetime.time(13, 29, 59, 716563), verbose_name='Horário da Análise'),
        ),
        migrations.AlterField(
            model_name='analiseproteina',
            name='horario',
            field=models.TimeField(default=datetime.time(13, 29, 59, 716377), verbose_name='Horário da Análise'),
        ),
        migrations.AlterField(
            model_name='analiseumidade',
            name='horario',
            field=models.TimeField(default=datetime.time(13, 29, 59, 715917), verbose_name='Horário da Análise'),
        ),
    ]
