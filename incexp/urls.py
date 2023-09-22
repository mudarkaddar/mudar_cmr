from django.urls import path
# from django.contrib import admin
from incexp import views
urlpatterns = [
path('', views.index, name='index'), 

]