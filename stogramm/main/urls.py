from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('singup/', views.singup, name='singup'),
    path('settings/', views.settings, name='settings'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('hot/', views.hot, name='hot'),
    # path('index/', views.index)
]
