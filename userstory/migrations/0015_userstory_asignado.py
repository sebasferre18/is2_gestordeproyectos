# Generated by Django 4.1 on 2022-11-02 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0014_alter_userstory_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='asignado',
            field=models.BooleanField(default=False),
        ),
    ]
