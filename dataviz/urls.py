from django.urls import path, include 
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('chart/', views.consumation_chart, name='consumation-chart'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('building_upload', views.building_upload, name="building_upload"),
    path('meter-upload', views.meter_upload, name="meter_upload"),
    path('halfhourly-upload', views.halfhourly_upload, name="halfhourly_upload"),
]
