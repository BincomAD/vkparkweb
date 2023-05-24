from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('', views.index),
    path('ask/', views.ask, name='ask'),
    path('index/', views.index),
    path('login/', views.login, name='login'),
    path('signup/', views.registration, name='signup'),
    path('settings', views.settings, name='settings'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('question/<int:question_id>/add_answer/', views.add_answer, name='add_answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

