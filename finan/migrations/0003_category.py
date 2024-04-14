# Generated by Django 5.0.4 on 2024-04-11 00:50

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finan', '0002_choice_question_delete_pessoa_choice_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None)),
                ('type_category', models.CharField(max_length=50)),
                ('classification', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
