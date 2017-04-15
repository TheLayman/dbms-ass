"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from myapp.views import hello, trending, addToPlayList, Like, playList
urlpatterns = [
   #Examples
   #url(r'^$', 'myproject.view.home', name = 'home'),
   #url(r'^blog/', include('blog.urls')),

   url(r'^admin', include(admin.site.urls)),
   url(r'^myapp/hello/$', hello, name = 'hello'),
   url(r'^myapp/trending/$', trending, name = 'trending'),
   url(r'^myapp/playList/$', playList, name = 'playList'),

   ## Ajax views
   url(r'^myapp/addToPlayList/$', addToPlayList, name = 'addToPlayList'),
   url(r'^myapp/Like/$', Like, name = 'Like'),

]
