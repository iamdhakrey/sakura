from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        avatar_url = "https://cdn.discordapp.com/avatars/"+str(request.user.id)+"/"+str(request.user.avatar)+".webp"
    else:
        avatar_url = None
    return render(request,'base.html',{'user':request.user,'avatar_url':avatar_url})