
from . import views
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    #path('/form', views.index, name='formPost'),
]

urlpatterns += staticfiles_urlpatterns()