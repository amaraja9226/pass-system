from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

#home page 

def home(request):
    return render(request, 'home.html')




#cretae application view




