# Generated by Django 4.1.4 on 2022-12-25 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_city_ip_address'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'ip_address')},
        ),
    ]
