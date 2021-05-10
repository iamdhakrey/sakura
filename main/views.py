from django.shortcuts import render

def home(request):
    return render(request,'base.html',{'user':request.user})