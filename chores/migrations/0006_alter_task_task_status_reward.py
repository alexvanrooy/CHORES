# Generated by Django 4.0.6 on 2022-08-09 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chores', '0005_alter_task_task_description_alter_task_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete'), ('Pending', 'Pending')], default='Incomplete', max_length=100),
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_title', models.CharField(max_length=100)),
                ('reward_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('reward_cost', models.PositiveIntegerField()),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chores.household')),
            ],
        ),
    ]