# Generated by Django 4.0.4 on 2022-06-12 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0006_rename_topic_subrecord_subtopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtopic',
            name='author',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название темы записи'),
        ),
        migrations.AlterField(
            model_name='subrecord',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/subrecords', verbose_name='Документ'),
        ),
        migrations.AlterField(
            model_name='subrecord',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/subrecords', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='subrecord',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название темы записи'),
        ),
    ]