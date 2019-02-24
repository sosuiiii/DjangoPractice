from django.urls import path
from . import views

app_name = 'timewire'

urlpatterns = [
    path('', views.index, name='register'),
    path('base/', views.base, name='base',),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('<int:id>/delete/', views.delete, name='delete'),
]
