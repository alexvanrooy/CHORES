# Generated by Django 4.0.6 on 2022-08-05 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chores', '0003_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chores.person'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
