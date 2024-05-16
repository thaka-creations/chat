from django.urls import path
from . import views

urlpatterns = [
   path('async_test', views.time_to_fetch, name='async_test'),
   path('generate-template', views.generate_template, name='generate_template')
]
