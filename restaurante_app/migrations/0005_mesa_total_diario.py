# Generated by Django 5.0.1 on 2024-03-06 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante_app', '0004_rename_ocupada_mesa_abierta_remove_mesa_numero_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesa',
            name='total_diario',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
