from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main_page_view),
    path('city/<name>', views.Weather_view, name='City'),
]