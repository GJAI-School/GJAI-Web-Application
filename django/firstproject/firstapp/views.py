from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("hello world!!!!!!") 

def login(request):
    return HttpResponse("로그인 되었습니다.")

def signout(request):
    return HttpResponse("잘가~!")
