# Generated by Django 4.1.6 on 2023-03-10 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0005_alter_rate_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='currency',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Euro'), (2, 'Dollar'), (3, 'Japanese yen'),
                                                            (4, 'British Pound Sterling'),
                                                            (5, 'Australian dollar')], default=2),
        ),
    ]