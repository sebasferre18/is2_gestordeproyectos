# Generated by Django 4.1 on 2022-11-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0016_rename_campo_userstory_estado_tarea_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
