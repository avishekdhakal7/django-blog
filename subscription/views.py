from django.shortcuts import render,redirect

from django.http import HttpResponse 

from django.contrib.auth.models import User, auth

from django.contrib import messages 

from django.core.mail import send_mail

from django.conf import settings

from .models import *


def subscription(request):
    return render(request,'index.html')