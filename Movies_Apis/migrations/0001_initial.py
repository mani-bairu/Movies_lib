# Generated by Django 3.2 on 2024-03-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('protagonists', models.TextField()),
                ('release_date', models.DateField()),
                ('status', models.CharField(choices=[('coming-up', 'coming-up'), ('starting', 'starting'), ('running', 'running'), ('finished', 'finished')], default='coming-up', max_length=100)),
                ('poster', models.ImageField(upload_to='posters')),
                ('trailer', models.FileField(upload_to='trailers')),
                ('rating', models.BigIntegerField()),
            ],
        ),
    ]
