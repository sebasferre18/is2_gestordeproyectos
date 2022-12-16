# Generated by Django 4.1 on 2022-12-16 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_usuario_id_alter_usuario_user'),
        ('proyectos', '0009_historial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('informacion', models.TextField(null=True)),
                ('visto', models.BooleanField()),
                ('destinatario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='usuarios.usuario')),
            ],
        ),
    ]
