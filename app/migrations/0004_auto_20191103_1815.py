# Generated by Django 2.2.6 on 2019-11-03 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191102_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='movies',
        ),
        migrations.AddField(
            model_name='movie',
            name='movies',
            field=models.ManyToManyField(to='app.Genre'),
        ),
    ]
