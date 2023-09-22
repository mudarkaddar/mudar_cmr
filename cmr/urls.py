from django.urls import path
# from django.contrib import admin
from cmr import views


# from txt_summary import functionat
urlpatterns = [
path('', views.index, name='index'), 

]