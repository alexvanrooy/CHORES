from msilib.schema import Feature
from django.contrib import admin
from .models import Household, Person, Task,Reward, ClaimedReward

# Register your models here.
admin.site.register(Household)
admin.site.register(Person)
admin.site.register(Task)
admin.site.register(Reward)
admin.site.register(ClaimedReward)
