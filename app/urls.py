from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_input, name='index'),
    path('app/static/<int:id>/example.txt', views.export_to_csv, name='export_to_csv'),
]

