# Generated by Django 5.0.1 on 2024-03-05 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante_app', '0003_cliente_ticket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mesa',
            old_name='ocupada',
            new_name='abierta',
        ),
        migrations.RemoveField(
            model_name='mesa',
            name='numero',
        ),
        migrations.AddField(
            model_name='mesa',
            name='cliente_identificacion',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='mesa',
            name='cliente_nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mesa',
            name='nombre',
            field=models.CharField(default=1111, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurante_app.mesa')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurante_app.producto')),
            ],
        ),
    ]