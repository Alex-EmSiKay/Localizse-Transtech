# Generated by Django 3.2.7 on 2021-12-11 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transtech', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='name',
            field=models.CharField(default='placeholder', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(max_length=2),
        ),
    ]
