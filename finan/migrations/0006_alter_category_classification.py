# Generated by Django 5.0.4 on 2024-04-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finan', '0005_alter_category_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='classification',
            field=models.CharField(choices=[('MI', 'Mista'), ('DE', 'Despesa'), ('RE', 'Receita')], default='MI', max_length=7),
        ),
    ]
