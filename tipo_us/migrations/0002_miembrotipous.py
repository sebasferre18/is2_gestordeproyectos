# Generated by Django 4.1 on 2022-09-25 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_alter_miembro_rol_alter_miembro_usuario'),
        ('tipo_us', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiembroTipoUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyecto')),
                ('tipo_us', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tipo_us.tipo_us')),
            ],
        ),
    ]
