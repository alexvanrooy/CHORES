from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Household(models.Model):
    house_name = models.CharField(max_length=100)
    house_code = models.CharField(max_length=20, unique=True)

    def generate_house_code():
        import random
        char_1 = chr(random.randint(65,90))
        char_2 = chr(random.randint(65,90))
        char_3 = chr(random.randint(65,90))
        dig_1 = str(random.randint(0,9))
        dig_2 = str(random.randint(0,9))
        dig_3 = str(random.randint(0,9))

        housecode = char_1 + char_2 + char_3 + dig_1 + dig_2 + dig_3
        return housecode

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(blank=True, null=True)

class Task(models.Model):
    TASK_STATUS_CHOICES = {
        ('Incomplete', 'Incomplete'),
        ('Pending','Pending'),
        ('Complete','Complete')
    }

    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length = 1000, blank = True, null=True)
    task_status = models.CharField(max_length=100, choices=TASK_STATUS_CHOICES, default='Incomplete')
    date_assigned = models.DateField()
    task_reward = models.PositiveIntegerField()
    completed_by = models.ForeignKey('Person', on_delete=models.CASCADE, null= True, blank=True )

class Reward(models.Model):
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    reward_title = models.CharField(max_length=100)
    reward_description = models.CharField(max_length = 1000, blank = True, null=True)
    reward_cost = models.PositiveIntegerField()

class ClaimedReward(models.Model):
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE)
    claimed_by = models.ForeignKey('Person', on_delete=models.CASCADE)