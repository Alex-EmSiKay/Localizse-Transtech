# Generated by Django 3.2.7 on 2021-12-14 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transtech', '0009_alter_user_secondary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='secondary',
            field=models.ManyToManyField(blank=True, related_name='secondary_users', to='transtech.Language'),
        ),
    ]
