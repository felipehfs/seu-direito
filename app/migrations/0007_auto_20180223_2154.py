# Generated by Django 2.0.2 on 2018-02-24 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180223_1910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposta',
            old_name='aceita',
            new_name='aceito',
        ),
    ]
