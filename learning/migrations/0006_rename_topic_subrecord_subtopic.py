# Generated by Django 4.0.4 on 2022-05-06 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0005_subtopic_subrecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subrecord',
            old_name='topic',
            new_name='subtopic',
        ),
    ]