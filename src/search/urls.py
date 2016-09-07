from django.conf.urls import url

import views

urlpatterns = [
    url(r'^api/search', views.search)
]
