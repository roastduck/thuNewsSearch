from django.conf.urls import url

import views

urlpatterns = [
    url(r'^api/search', views.search),
    url(r'^$', 'django.contrib.staticfiles.views.serve', kwargs = { 'path': 'index.html' })
]

