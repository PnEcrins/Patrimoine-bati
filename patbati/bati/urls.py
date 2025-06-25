from patbati.bati import models
from mapentity.registry import registry
from django.urls import path
from patbati.bati.views import EnquetesCreate, PerspectiveCreate

app_name = "bati"

urlpatterns = registry.register(models.Bati)
urlpatterns += [
    path('bati/<int:pk>/enquetes/add/', EnquetesCreate.as_view(), name='enquetes_add'),
    path('bati/<int:pk>/perspective/add/', PerspectiveCreate.as_view(), name='perspectives_add'),
]