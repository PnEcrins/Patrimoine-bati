from patbati.bati import models
from mapentity.registry import registry
from django.urls import path
from patbati.bati.views import DemandeTravauxCreate, DemandeTravauxDelete, DemandeTravauxUpdate, EnquetesCreate, EnquetesUpdate, EnquetesDelete, PerspectiveCreate, PerspectiveDelete, PerspectiveUpdate, TravauxCreate, TravauxDelete, TravauxUpdate

app_name = "bati"

urlpatterns = registry.register(models.Bati)
urlpatterns += [
    path('bati/<int:pk>/enquetes/add/', EnquetesCreate.as_view(), name='enquetes_add'),
    path('bati/<int:pk>/enquetes/<int:enquete_pk>/update/', EnquetesUpdate.as_view(), name='enquetes_update'),
    path('bati/<int:pk>/enquetes/<int:enquete_pk>/delete/', EnquetesDelete.as_view(), name='enquetes_delete'),
    
    path('bati/<int:pk>/perspective/add/', PerspectiveCreate.as_view(), name='perspectives_add'),
    path('bati/<int:pk>/perspective/<int:perspective_pk>/update/', PerspectiveUpdate.as_view(), name='perspectives_update'),
    path('bati/<int:pk>/perspective/<int:perspective_pk>/delete/', PerspectiveDelete.as_view(), name='perspectives_delete'),
    
    path('bati/<int:pk>/demande_travaux/add/', DemandeTravauxCreate.as_view(), name='demande_travaux_add'),
    path('bati/<int:pk>/demande_travaux/<int:demande_pk>/update/', DemandeTravauxUpdate.as_view(), name='demande_travaux_update'),
    path('bati/<int:pk>/demande_travaux/<int:demande_pk>/delete/', DemandeTravauxDelete.as_view(), name='demande_travaux_delete'),
    
    path('bati/<int:pk>/travaux/add/', TravauxCreate.as_view(), name='travaux_add'),
    path('bati/<int:pk>/travaux/<int:travaux_pk>/update/', TravauxUpdate.as_view(), name='travaux_update'),
    path('bati/<int:pk>/travaux/<int:travaux_pk>/delete/', TravauxDelete.as_view(), name='travaux_delete'),
]