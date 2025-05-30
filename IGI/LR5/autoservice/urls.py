"""
URL configuration for autoservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('about/', include('main.urls')),
    path('news/', include('main.urls')),
    path('faq/', include('main.urls')),
    path('contacts/', include('main.urls')),
    path('politcy/', include('main.urls')),
    path('vacancy/', include('main.urls')),
    path('reviews/', include('main.urls')),
    path('coupons/', include('main.urls')), 
    path('login/', include('main.urls')),
    path('register/', include('main.urls')),
    path('settings/', include('main.urls')),
    path('cataloge/', include('main.urls')),
    path('master_schedule/', include('main.urls')),
    path('review_list/create_review/', include('main.urls')),
]
