# Generated by Django 2.2 on 2019-05-01 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecproduct', '0003_auto_20190430_2156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['created_at'], 'permissions': (('onlyread', 'onlyread'), ('can_create', 'can_create'), ('readwrite', 'readwrite'))},
        ),
    ]