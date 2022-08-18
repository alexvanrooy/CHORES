from django import forms

ACCOUNT_CHOICES = (
    ("Parent","Parent"),
    ("Child","Child"),
)

class RegisterForm(forms.Form):
    first_name = forms.CharField(label= 'First Name', max_length=100)
    username = forms.CharField(label= 'Username', max_length=100)
    password1 = forms.CharField(label='Password',max_length=100,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',max_length=100,widget=forms.PasswordInput)
    account_type = forms.ChoiceField(choices = ACCOUNT_CHOICES)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password',max_length=100,widget=forms.PasswordInput)

class TaskForm(forms.Form):
    task_title = forms.CharField(label = 'Task Title', max_length=100)
    task_description = forms.CharField(label = 'Task Description', max_length=1000, required=False)
    task_reward = forms.IntegerField(label = 'Reward')

class RewardForm(forms.Form):
    reward_title = forms.CharField(label = 'Reward Title', max_length=100)
    reward_description = forms.CharField(label = 'Reward Description',max_length = 1000, required=False)
    reward_cost = forms.IntegerField(label = 'Cost')