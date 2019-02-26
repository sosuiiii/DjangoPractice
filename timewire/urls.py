from django.urls import path
from . import views

app_name = 'timewire'

urlpatterns = [
    path('', views.index, name='register'),
    path('base/', views.base, name='base',),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myPage/', views.myPage, name='myPage'),
    path('detail/<int:work_id>', views.detail, name='detail'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('update/<int:pk>', views.update, name='update'),
]
