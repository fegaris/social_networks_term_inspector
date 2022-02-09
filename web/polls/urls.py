
from . import views
from django.urls import path, include

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    #path('/form', views.index, name='formPost'),
]

