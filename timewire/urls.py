from django.urls import path
from . import views

app_name = 'timewire'

urlpatterns = [
    path('', views.index, name='register'),
    path('base/', views.base, name='base',),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myPage/', views.myPage, name='myPage'),
    path('grant/', views.grant, name='grant'),
    path('work/', views.work, name='work'),
    path('favorite/', views.favorite, name='favorite'),
    path('bank/', views.bank, name='bank'),
    path('value/', views.value, name='value'),
    path('question/', views.question, name='question'),
    path('setting/', views.setting, name='setting'),
    path('term/', views.term, name='term'),
    path('ranking/', views.ranking, name='ranking'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('detail/<int:work_id>', views.detail, name='detail'),
    path('index/', views.index, name='index'),
    path('search', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('update/<int:pk>', views.update, name='update'),
]
