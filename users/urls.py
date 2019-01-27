from django.urls import path
from django.conf.urls import url
from . import views
#see for its name

#see this if special charactes don't work
#https://stackoverflow.com/questions/1739431/allow-in-django-url
#[a-zA-Z0-9]
urlpatterns = [
    url (r'profile/(?P<username>[\w.@+_-]+)$',views.get_user_profile,name='user_profile'),
]
