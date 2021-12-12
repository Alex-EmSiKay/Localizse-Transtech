# Generated by Django 3.2.7 on 2021-12-11 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transtech', '0002_auto_20211211_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_pri',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_users_active', to='transtech.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='active_sec',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_users_active', to='transtech.language'),
        ),
        migrations.AlterField(
            model_name='user',
            name='primary',
            field=models.ManyToManyField(related_name='primary_users', to='transtech.Language'),
        ),
        migrations.AlterField(
            model_name='user',
            name='secondary',
            field=models.ManyToManyField(related_name='secondary_users', to='transtech.Language'),
        ),
    ]