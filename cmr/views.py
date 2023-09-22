from django.shortcuts import render

# Create your views here.

def index(request):
   return  render(request, 'cmr/index.html', {'message':'1'})