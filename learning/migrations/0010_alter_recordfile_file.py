# Generated by Django 4.0.7 on 2023-03-30 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0009_subrecordfile_recordfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfile',
            name='file',
            field=models.FileField(upload_to='documents/records/', verbose_name='Доп. документ'),
        ),
    ]