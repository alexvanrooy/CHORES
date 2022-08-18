from django.urls import path
from . import views

app_name = 'chores'
urlpatterns = [ 
    path('',views.index, name = 'index'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout, name = 'logout'),
    path('register/',views.register, name = 'register'),
    path('home/',views.home, name = 'home'),
    path('createhouse/', views.createhouse, name = 'createhouse'),
    path('createtask/', views.createtask, name = 'createtask'),
    path('tasks/', views.tasks, name = 'tasks'),
    path('tasks/delete/<int:task_id>', views.deletetask, name = 'deletetask'),
    path('rewards/', views.rewards, name = 'rewards'),
    path('createreward/', views.createreward, name = 'createreward'),
    path('rewards/delete/<int:reward_id>', views.deletereward, name = 'deletereward'),
    path('joinhouse/', views.joinhouse, name = 'joinhouse'),
    path('home/complete/<int:task_id>', views.completetask, name = 'completetask'),
    path('home/approve/<int:task_id>', views.approvetask, name = 'approvetask'),
    path('home/deny/<int:task_id>', views.denytask, name = 'denytask'), 
    path('home/claim/<int:reward_id>', views.claimreward, name = 'claimreward'),
    path('home/acknowledge/<int:claimed_reward_id>',views.acknowledgereward, name = 'acknowledgereward')

]