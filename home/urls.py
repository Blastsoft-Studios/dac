from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib import admin
from dac.settings import STATIC_URL

import home.views as home

urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=STATIC_URL + 'favicon.ico'
    )),
    url(r'^avatar/$', home.avatar, name="avatar"),
    url(r'^admin/', admin.site.urls, name="django_admin"),
]
