# Generated by Django 4.1.6 on 2023-05-20 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_alter_rate_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ('-created',)},
        ),
    ]