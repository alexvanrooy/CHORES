# Generated by Django 4.0.6 on 2022-08-10 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chores', '0006_alter_task_task_status_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='balance',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
