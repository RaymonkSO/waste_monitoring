# Generated by Django 5.1.3 on 2024-11-14 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filllevel',
            old_name='timestamp',
            new_name='fill_date',
        ),
        migrations.RenameField(
            model_name='weightlevel',
            old_name='weight',
            new_name='weight_level',
        ),
    ]
