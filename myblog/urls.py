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
from myapp.views import register, login, logout, hello, trending, addToPlayList, Like, playList, removeFromPlayList, unLike
urlpatterns = [
   #Examples
   #url(r'^$', 'myproject.view.home', name = 'home'),
   #url(r'^blog/', include('blog.urls')),

   url(r'^admin', include(admin.site.urls)),
   url(r'^register/$', register, name = 'register'),
   url(r'^login/$', login, name = 'login'),
   url(r'^logout/$', logout, name = 'logout'),
   url(r'^hello/$', hello, name = 'hello'),
   url(r'^trending/$', trending, name = 'trending'),
   url(r'^playList/$', playList, name = 'playList'),
   url(r'^$', hello, name = 'hello'),

   ## Ajax views
   url(r'^addToPlayList/$', addToPlayList, name = 'addToPlayList'),
   url(r'^removeFromPlayList/$', removeFromPlayList, name = 'removeFromPlayList'),
   url(r'^Like/$', Like, name = 'Like'),
   url(r'^unLike/$',unLike, name = 'unLike'),

]
