"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from main.views import home,new_home
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from sakura.views import dashboard, enable_welcome_msg,server, welcome ,CommandView,WelcomeView

urlpatterns = [
    path('auth/',include('sakuralogin.urls')),
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('new',new_home,name='new_home'),
    path('dashboard/',dashboard,name='dashboard' ),
    path('server/<int:pk>',server,name='server'),
    path('background.css', TemplateView.as_view(
        template_name='background.css',
        content_type='text/css')
    ),
    path('command/',CommandView.as_view(template_name="command.html"),name='command'),

    ############### Welcome #####################
    path('server/<int:pk>/welcome',welcome,name='welcome'),
    path('server/<int:pk>/welcome/enable',enable_welcome_msg,name='enable'),
    
    
    # test
    # path('welcome/<int:pk>',WelcomeView.as_view(template_name="welcome.html"),name='welcome'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
