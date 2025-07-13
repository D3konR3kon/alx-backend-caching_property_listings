from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [

    path('', views.property_list, name='property_list'),
    path('<int:property_id>/', views.property_detail, name='property_detail'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
]