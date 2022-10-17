# Generated by Django 4.1 on 2022-10-16 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0004_alter_miembro_rol'),
        ('tipo_us', '0003_tipo_us_campos'),
        ('sprints', '0001_initial'),
        ('userstory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='prioridad',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userstory',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sprints.sprint'),
        ),
        migrations.AddField(
            model_name='userstory',
            name='sprint_previo',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='userstory',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='proyectos.miembro'),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='autor',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='tipo_us',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tipo_us.miembrotipous'),
        ),
    ]
