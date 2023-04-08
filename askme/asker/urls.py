from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ask/', views.ask, name='ask'),
    path('index/', views.index),
    path('login/', views.login, name='login'),
    path('signup/', views.registration, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
]
