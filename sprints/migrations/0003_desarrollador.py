# Generated by Django 4.1 on 2022-10-29 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0014_alter_userstory_descripcion'),
        ('proyectos', '0009_remove_miembro_capacidad'),
        ('sprints', '0002_sprint_fecha_fin_sprint_fecha_inicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desarrollador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad', models.IntegerField(default=0)),
                ('miembro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.miembro')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprints.sprint')),
                ('userstory', models.ManyToManyField(blank=True, to='userstory.userstory')),
            ],
        ),
    ]
