# Generated by Django 4.1 on 2022-09-25 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0005_rol_proyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
