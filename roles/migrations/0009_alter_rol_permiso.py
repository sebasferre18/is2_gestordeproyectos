# Generated by Django 4.1 on 2022-11-04 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0008_permiso_es_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='permiso',
            field=models.ManyToManyField(blank=True, to='roles.permiso'),
        ),
    ]
