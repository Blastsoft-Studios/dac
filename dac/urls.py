from django.conf.urls import url
from django.contrib import admin

import home.views as home

urlpatterns = [
	url(r'^$', home.home, name='home'),
	url(r'^avatar/', home.avatar, name="avatar"),
	url(r'^admin/', admin.site.urls, name="django_admin"),
]
