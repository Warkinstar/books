# Generated by Django 4.0.7 on 2023-03-30 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Отчество'),
        ),
    ]
