# Generated by Django 4.1 on 2022-12-13 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0013_alter_historial_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='story_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='historial',
            name='accion',
            field=models.CharField(choices=[('Creacion', 'Creacion'), ('Modificacion', 'Modificacion'), ('Eliminacion', 'Eliminacion'), ('Importacion', 'Importacion')], max_length=25, null=True),
        ),
    ]
