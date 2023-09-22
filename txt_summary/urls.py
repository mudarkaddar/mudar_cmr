from django.urls import path
# from django.contrib import admin
from txt_summary import views
# from txt_summary import functionat
urlpatterns = [
path('', views.index, name='index'),   
path('prog/', views.prog, name='prog'),
path('parameter_selection/', views.get_params, name='parameter_selection'),
path('signup/', views.signup, name='signup'),
path('act/<token>/<uidb64>', views.activate, name='activate'),
path('login/', views.logain, name='login'),
path('signout/', views.signout, name='signout'),
path('parameter_selection_abstract/', views.get_params_abstract, name='parameter_selection_abstract'),
path('parameter_selection_abstract2/', views.get_params_abstract2, name='parameter_selection_abstract2'),

]   