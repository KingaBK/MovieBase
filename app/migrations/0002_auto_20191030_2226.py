# Generated by Django 2.2.6 on 2019-10-30 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='movies',
            new_name='movie',
        ),
    ]
