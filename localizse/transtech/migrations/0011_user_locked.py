# Generated by Django 3.2.7 on 2021-12-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transtech', '0010_alter_user_secondary'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]
