from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('analises', '0003_alter_analiseproteina_horario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analiseproteina',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de Criação'),
        ),
        migrations.AddField(
            model_name='analiseproteina',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Última Atualização'),
        ),
        migrations.AddField(
            model_name='analiseumidade',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de Criação'),
        ),
        migrations.AddField(
            model_name='analiseumidade',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Última Atualização'),
        ),
    ]
