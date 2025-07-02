from ast import Delete
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mapentity.views.generic import (
    MapEntityList, MapEntityDetail,
    MapEntityFormat, MapEntityCreate, MapEntityUpdate, MapEntityDocument,
    MapEntityDelete
)
from mapentity.views.api import MapEntityViewSet
from mapentity.views.mixins import ModelViewMixin
from patbati.bati.forms import DemandeTravauxForm, EnquetesForm, BatiForm, PerspectiveForm, TravauxForm
from .models import Bati, DemandeTravaux, Enquetes, Perspective, Travaux
from .serializers import BatiSerializer, BatiGeojsonSerializer
from patbati.mapentitycommon.forms import FormsetMixin
from patbati.mapentitycommon.views import ChildFormViewMixin
# Create your views here.


def home(request):
    return HttpResponse("YEP")


class BatiList(MapEntityList):
    model = Bati
    columns = [
        "id",
        "valide",
        "appelation",
        "secteur",
        "notepatri",
        "conservation",
        "date_update"
    ]

class BatiDetail(MapEntityDetail):
    model = Bati

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapwidth"] = "90%"
        return context


# class BatiCreate(FormsetMixin, MapEntityCreate):
#     model = Bati
#     context_name = 'demande_travaux_formset'
#     form_class = BatiForm
#     formset_class = DemandeTravauxFormSet



class BatiCreate(MapEntityCreate):
    model = Bati
    form_class = BatiForm



class BatiFormat(MapEntityFormat, BatiList):
    pass

class BatiViewSet(MapEntityViewSet):
    model = Bati
    serializer_class = BatiSerializer
    geojson_serializer_class = BatiGeojsonSerializer

    queryset = Bati.objects.all()


class EnquetesCreate(ChildFormViewMixin, CreateView):
    model = Enquetes
    parent_model = Bati
    parent_related_name = "bati"
    form_class = EnquetesForm
    add_label = "Nouvelle"

class EnquetesUpdate(ChildFormViewMixin, UpdateView):
    model = Enquetes
    parent_model = Bati
    parent_related_name = "bati"
    form_class = EnquetesForm
    add_label = "Modifier l'enquête"
    pk_url_kwarg = 'enquete_pk'

class EnquetesDelete(ChildFormViewMixin, DeleteView):
    model = Enquetes
    parent_model = Bati
    parent_related_name = "bati"
    form_class = EnquetesForm
    add_label = "Supprimer l'enquête"
    pk_url_kwarg = 'enquete_pk'

class PerspectiveCreate(ChildFormViewMixin, CreateView):
    model = Perspective
    parent_model = Bati
    form_class = PerspectiveForm
    parent_related_name = "bati"
    add_label = "Nouvel"

class PerspectiveUpdate(ChildFormViewMixin, UpdateView):
    model = Perspective
    parent_model = Bati
    form_class = PerspectiveForm
    parent_related_name = "bati"
    add_label = "Modifier la perspective"
    pk_url_kwarg = 'perspective_pk'

class PerspectiveDelete(ChildFormViewMixin, DeleteView):
    model = Perspective
    parent_model = Bati
    form_class = PerspectiveForm
    parent_related_name = "bati"
    add_label = "Supprimer la perspective"
    pk_url_kwarg = 'perspective_pk'

class DemandeTravauxCreate(ChildFormViewMixin, CreateView):
    model = DemandeTravaux
    parent_model = Bati
    form_class = DemandeTravauxForm
    parent_related_name = "bati"
    add_label = "Nouvelle demande de travaux"

class DemandeTravauxUpdate(ChildFormViewMixin, UpdateView):
    model = DemandeTravaux
    parent_model = Bati
    form_class = DemandeTravauxForm
    parent_related_name = "bati"
    add_label = "Modifier la demande de travaux"
    pk_url_kwarg = 'demande_pk'

class DemandeTravauxDelete(ChildFormViewMixin, DeleteView):
    model = DemandeTravaux
    parent_model = Bati
    form_class = DemandeTravauxForm
    parent_related_name = "bati"
    add_label = "Supprimer la demande de travaux"
    pk_url_kwarg = 'demande_pk'
    template_name = "bati/demandetravaux_delete.html"

class TravauxCreate(ChildFormViewMixin, CreateView):
    model = Travaux
    parent_model = Bati
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Nouveau travaux"

class TravauxUpdate(ChildFormViewMixin, UpdateView):
    model = Travaux
    parent_model = Bati
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Modifier les travaux: "
    pk_url_kwarg = 'travaux_pk'

class TravauxDelete(ChildFormViewMixin, DeleteView):
    model = Travaux
    parent_model = Bati
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Supprimer les travaux: "
    pk_url_kwarg = 'travaux_pk'
    template_name = "bati/travaux_delete.html"


    
    