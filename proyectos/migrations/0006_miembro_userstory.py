# Generated by Django 4.1 on 2022-10-17 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userstory', '0011_remove_userstory_usuario'),
        ('proyectos', '0005_miembro_capacidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='userstory',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='userstory.userstory'),
        ),
    ]
