# Generated manually for Sprint 5.

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Brokerage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('name', models.CharField(max_length=150, verbose_name='nome')),
                ('legal_name', models.CharField(max_length=200, verbose_name='razão social')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('plan', models.CharField(choices=[('free', 'Free')], default='free', max_length=20, verbose_name='plano')),
                ('is_active', models.BooleanField(default=True, verbose_name='ativa')),
            ],
            options={
                'verbose_name': 'corretora',
                'verbose_name_plural': 'corretoras',
                'ordering': ('name',),
            },
        ),
    ]
