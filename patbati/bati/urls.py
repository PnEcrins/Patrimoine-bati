from patbati.bati import models
from mapentity.registry import registry
from django.urls import path
from patbati.bati.views import EnquetesCreate

app_name = "bati"

urlpatterns = registry.register(models.Bati)
urlpatterns += [
    path('bati/<int:bati_pk>/enquetes/add/', EnquetesCreate.as_view(), name='enquetes_add'),
]