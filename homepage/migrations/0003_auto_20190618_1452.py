# Generated by Django 2.2 on 2019-06-18 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20190616_2353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id']},
        ),
    ]
