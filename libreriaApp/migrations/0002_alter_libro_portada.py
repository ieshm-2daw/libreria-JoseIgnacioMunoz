# Generated by Django 3.2.23 on 2023-11-28 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreriaApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(blank=True, null=True, upload_to='portadas/'),
        ),
    ]
