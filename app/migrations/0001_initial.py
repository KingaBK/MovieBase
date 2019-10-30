# Generated by Django 2.2.6 on 2019-10-30 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.UUIDField(editable=False, unique=True)),
                ('title', models.CharField(editable=False, max_length=50, unique=True)),
                ('year', models.IntegerField()),
                ('runtime', models.IntegerField()),
                ('director', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=50, unique=True)),
                ('movies', models.ManyToManyField(to='app.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Movie')),
            ],
        ),
    ]