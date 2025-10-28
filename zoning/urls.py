from django.urls import path

from . import views

app_name = 'zoning'

urlpatterns = [
    path('api/<str:area_type>/areas.geojson', views.ZoningGeoJsonViewList.as_view(), name="zoning_layer"),
]
