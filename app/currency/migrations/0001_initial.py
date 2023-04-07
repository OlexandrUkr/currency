# Generated by Django 4.1.6 on 2023-04-04 21:21

import currency.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('email_from', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RequestResponseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('request_method', models.CharField(max_length=10)),
                ('time', models.DecimalField(decimal_places=20, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('code_name', models.CharField(max_length=64, unique=True)),
                ('source_logo', models.FileField(blank=True,
                                                 default=None,
                                                 null=True,
                                                 upload_to=currency.models.source_path)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('currency', models.PositiveSmallIntegerField(
                    choices=[(1, 'Euro'),
                             (2, 'Dollar'),
                             (3, 'Japanese yen'),
                             (4, 'British Pound Sterling'),
                             (5, 'Australian dollar')],
                    default=2)),
                ('buy', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sale', models.DecimalField(decimal_places=2, max_digits=6)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.source')),
            ],
        ),
    ]
