# Generated by Django 5.0.4 on 2024-06-28 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferencia',
            old_name='data_tranferencia',
            new_name='data_transferencia',
        ),
    ]