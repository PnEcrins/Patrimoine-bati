from patbati.bati import models
from mapentity.registry import registry
from django.urls import path
from patbati.bati.views import DemandeTravauxCreate, DemandeTravauxDelete, DemandeTravauxUpdate, EnquetesCreate, EnquetesUpdate, EnquetesDelete, PerspectiveCreate, PerspectiveDelete, PerspectiveUpdate, SecondOeuvreCreate, SecondOeuvreDelete, SecondOeuvreFinitionCreate, SecondOeuvreFinitionDelete, SecondOeuvreFinitionUpdate, SecondOeuvreUpdate, StructureCreate, StructureDelete, StructureFinitionCreate, StructureFinitionDelete, StructureFinitionUpdate, StructureUpdate, TravauxCreate, TravauxDelete, TravauxUpdate

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
    
    path('bati/<int:pk>/demande_travaux/<int:demande_pk>/travaux/add/', TravauxCreate.as_view(), name='travaux_add'),
    path('bati/<int:pk>/travaux/<int:travaux_pk>/update/', TravauxUpdate.as_view(), name='travaux_update'),
    path('bati/<int:pk>/travaux/<int:travaux_pk>/delete/', TravauxDelete.as_view(), name='travaux_delete'),

    path('bati/<int:pk>/structure/add/', StructureCreate.as_view(), name='structure_add'),
    path('bati/<int:pk>/structure/<int:structure_pk>/update/', StructureUpdate.as_view(), name='structure_update'),
    path('bati/<int:pk>/structure/<int:structure_pk>/delete/', StructureDelete.as_view(), name='structure_delete'),

    path('bati/<int:pk>/second/add/', SecondOeuvreCreate.as_view(), name='second_add'),
    path('bati/<int:pk>/second/<int:second_pk>/update/', SecondOeuvreUpdate.as_view(), name='second_update'),
    path('bati/<int:pk>/second/<int:second_pk>/delete/', SecondOeuvreDelete.as_view(), name='second_delete'),

    path('bati/<int:pk>/structure/<int:structure_pk>/finition/add/', StructureFinitionCreate.as_view(), name='structure_finition_add'),
    path('bati/<int:pk>/structure/<int:structure_pk>/finition/<int:struct_finition_pk>/update/', StructureFinitionUpdate.as_view(), name='structure_finition_update'),
    path('bati/<int:pk>/structure/<int:structure_pk>/finition/<int:struct_finition_pk>/delete/', StructureFinitionDelete.as_view(), name='structure_finition_delete'),

    path('bati/<int:pk>/second_oeuvre/<int:second_pk>/finition/add/', SecondOeuvreFinitionCreate.as_view(), name='second_finition_add'),
    path('bati/<int:pk>/second_oeuvre/<int:second_pk>/finition/<int:so_finition_pk>/update/', SecondOeuvreFinitionUpdate.as_view(), name='second_finition_update'),
    path('bati/<int:pk>/second_oeuvre/<int:second_pk>/finition/<int:so_finition_pk>/delete/', SecondOeuvreFinitionDelete.as_view(), name='second_finition_delete'),
]