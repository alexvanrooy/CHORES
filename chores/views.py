from binascii import Incomplete
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from .models import Household, Person, Task, Reward, ClaimedReward
from .forms import RegisterForm, LoginForm, TaskForm, RewardForm

import datetime

# Constants

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/index.html')
    
    return home(request)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('../home')
            else:
                context = {
                    'form' : form,
                    'error' : "Invalid login. Please try again."
                }
                return render(request,'chores/login.html', context)
    else:
        form = LoginForm()
    return render(request, 'chores/login.html', {'form' : form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            password2 =form.cleaned_data.get("password2")
            account_type = form.cleaned_data.get("account_type")
            try:
                user = User.objects.get(username = username)
                context = {
                    'form' : form,
                    'error' : "The username you have entered already exists. Please try again."
                }
                return render(request,'chores/register.html', context) 
            except User.DoesNotExist:
                if password1 != password2:
                    context = {
                        'form' : form,
                        'error' : "Passwords do not match."
                    }
                    return render(request,'chores/register.html', context) 
                else:
                    user = User.objects.create_user(username = username, email = None, password = password1)
                    user.first_name = first_name
                    user.save()
                    account_group = Group.objects.get(name = account_type)
                    account_group.user_set.add(user)
                    
                    return HttpResponseRedirect('../login')
    else:
        form = RegisterForm()
    return render(request,'chores/register.html', {'form' : form})

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')
    current_user = request.user

    try:
        person = Person.objects.get(pk = current_user.id)
        has_household = True

        assigned_tasks = Task.objects.filter(household = person.household)
        rewards = Reward.objects.filter(household = person.household)
        claimed_rewards = ClaimedReward.objects.filter(household = person.household)



        context = {
            'user_name' : current_user.first_name,
            'has_household' : has_household,
            'household_name' : person.household.house_name,
            'tasks' : assigned_tasks,
            'house_code' : person.household.house_code,
            'rewards' : rewards,
            'balance' : person.balance,
            'claimed_rewards' : claimed_rewards
        }

    except Person.DoesNotExist:
        has_household = False

        context = {
            'user_name' : current_user.first_name,
            'has_household' : has_household
        }
    
    if current_user.groups.filter(name = 'Parent'):
        return render(request, 'chores/home_parent.html', context)
    elif current_user.groups.filter(name = 'Child'):
        return render(request, 'chores/home_child.html', context)

def createhouse(request):

    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')
    
    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
        return home(request)
    except Person.DoesNotExist:
        pass

    temp_code = Household.generate_house_code()

    if request.method == 'POST':
        house_name = request.POST['house_name']
        
        unique_code = False
        while unique_code == False:
            try:
                existing_house = Household.objects.get(house_code = temp_code)
            except Household.DoesNotExist:
                unique_code = True
        
        new_house = Household(house_name = house_name, house_code = temp_code)
        new_house.save()

        new_person = Person(request.user.id, new_house.id)
        new_person.save()
        
        return HttpResponseRedirect('../home')

    return render(request, 'chores/household_creation.html')

def createtask(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_title = form.cleaned_data.get('task_title')
            task_description = form.cleaned_data.get('task_description')
            task_reward = form.cleaned_data.get('task_reward')

            if(task_reward < 0):
                context = {
                    'form' : form,
                    'error' : 'Reward cannot be negative.',
                }
                return render(request, 'chores/task_creation.html', context)  
            else:
                household = person.household
                current_date = datetime.date.today()

                new_task = Task(
                    household = household,
                    task_title = task_title,
                    task_description = task_description,
                    date_assigned = current_date,
                    task_reward = task_reward
                )
                new_task.save()
                return HttpResponseRedirect('../home')

    else:
        form = TaskForm()

    return render(request, 'chores/task_creation.html', {'form':form}) 

def tasks(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)

    house_tasks = Task.objects.filter(household = person.household)

    context = {
        'tasks' : house_tasks, 
    }
    
    return render(request, 'chores/tasks.html', context)

def deletetask(request, task_id):
    #TODO: restrict access to this so only the parent of the household can delete the task

    Task.objects.filter(pk = task_id).delete()

    
    return HttpResponseRedirect('../')

def rewards(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)

    house_rewards = Reward.objects.filter(household = person.household)

    context = {
        'rewards' : house_rewards, 
    }
    return render(request, 'chores/rewards.html', context)

def createreward(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            reward_title = form.cleaned_data.get('reward_title')
            reward_description = form.cleaned_data.get('reward_description')
            reward_cost = form.cleaned_data.get('reward_cost')

            if(reward_cost < 0):
                context = {
                    'form' : form,
                    'error' : 'Cost cannot be negative.',
                }
                return render(request, 'chores/rewards_creation.html', context)  
            else:
                household = person.household

                new_reward = Reward(
                    household = household,
                    reward_title = reward_title,
                    reward_description = reward_description,
                    reward_cost = reward_cost
                )

                new_reward.save()
                return HttpResponseRedirect('../home')

    else:
        form = RewardForm()

    return render(request, 'chores/rewards_creation.html', {'form' : form})

def deletereward(request, reward_id):
    #TODO: restrict access to this so only the parent of the household can delete the reward

    Reward.objects.filter(pk = reward_id).delete()

    
    return HttpResponseRedirect('../')

def joinhouse(request):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')
    
    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
        return home(request)
    except Person.DoesNotExist:
        pass
    
    if request.method == 'POST':
        house_code = request.POST['house_code']

        try:
            household = Household.objects.get(house_code = house_code)
        except Household.DoesNotExist:
            error_message = "No household exists with that code. Please try again."
            return home(request)

        new_person = Person(current_user.id,household.id, balance = 0)
        new_person.save()

        return HttpResponseRedirect('../')

    return render(request, 'chores/home_child.html')

def completetask(request, task_id):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)

    task = Task.objects.get(pk = task_id)
    task.task_status = 'Pending'
    task.completed_by = person
    task.save()

    return HttpResponseRedirect('../')

def approvetask(request, task_id):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    

    task = Task.objects.get(pk = task_id)
    child = task.completed_by
    child.balance += task.task_reward
    
    child.save()

    task.delete()

    return HttpResponseRedirect('../')

def denytask(request, task_id):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    

    task = Task.objects.get(pk = task_id)

    task.completed_by = None
    task.task_status = 'Incomplete'
    task.save()

    return HttpResponseRedirect('../')

def claimreward(request, reward_id):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    
    reward = Reward.objects.get(pk = reward_id)

    if(person.balance >= reward.reward_cost):
        claimed_reward = ClaimedReward(
            household = person.household,
            reward = reward,
            claimed_by = person
        )
        
        person.balance -= reward.reward_cost

        person.save()
        claimed_reward.save()
    return HttpResponseRedirect('../')

def acknowledgereward(request, claimed_reward_id):
    if not request.user.is_authenticated:
        return render(request, 'chores/login_error.html')

    current_user = request.user
    try:
        person = Person.objects.get(pk = current_user.id)
    except Person.DoesNotExist:
        return home(request)
    
    claimed_reward = ClaimedReward.objects.filter(pk = claimed_reward_id).delete()

    return HttpResponseRedirect('../')