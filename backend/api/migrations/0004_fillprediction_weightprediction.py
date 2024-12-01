# Generated by Django 5.1.3 on 2024-11-14 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_filllevel_fill_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FillPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_level', models.FloatField(null=True)),
                ('fill_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WeightPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_level', models.FloatField(null=True)),
                ('weight_time', models.TimeField()),
            ],
        ),
    ]