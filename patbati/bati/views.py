from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mapentity.views.generic import (
    MapEntityList,
    MapEntityDetail,
    MapEntityFormat,
    MapEntityCreate,
    MapEntityUpdate,
    MapEntityDocument,
    MapEntityDelete,
)
from django.db.models.functions import Coalesce
from django.db.models import Value, DateField
from mapentity.views.api import MapEntityViewSet
from mapentity.views.mixins import ModelViewMixin
from patbati.bati.filters import BatiFilterSet

from patbati.bati.forms import (
    DemandeTravauxForm,
    EnquetesForm,
    BatiForm,
    IllustrationForm,
    MateriauFinFinitionSecondOeuvreForm,
    PerspectiveForm,
    SecondOeuvreForm,
    MateriauFinFinitionStructureForm,
    StructureForm,
    TravauxForm,
)
from .models import (
    Bati,
    DemandeTravaux,
    Enquetes,
    Illustration,
    MateriauxFinFinitionSecondOeuvre,
    MateriauxFinFinitionStructure,
    Perspective,
    SecondOeuvre,
    Structure,
    Travaux,
)
from .serializers import BatiSerializer, BatiGeojsonSerializer
from patbati.mapentitycommon.forms import FormsetMixin
from patbati.mapentitycommon.views import ChildFormViewMixin, ChildDeleteViewMixin
from mapentity.views import MapEntityFilter

# Create your views here.


def home(request):
    return HttpResponse("YEP")


class BatiFilter(MapEntityFilter):
    model = Bati
    filterset_class = BatiFilterSet


class BatiList(MapEntityList):
    queryset = Bati.objects.all()
    columns = [
        "id",
        "valide",
        "appelation",
        "type_bat",
        "notepatri",
        "conservation",
        "date_update",
    ]
    searchable_columns = [
        "appelation",
        "type_bat__label",
        "notepatri__label",
        "conservation__label",
    ]

    filterform = BatiFilter


class BatiDetail(MapEntityDetail):
    model = Bati

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapwidth"] = "90%"

        # Sort demandes_travaux by date_demande_permis (nulls last)
        demandes = (
            self.object.demandes_travaux.all()
            .annotate(
                date_sort=Coalesce(
                    "date_demande_permis", Value("0001-01-01", output_field=DateField())
                )
            )
            .order_by("-date_sort")
        )

        # For each demande, sort travaux by date (nulls last)
        demandes_travaux_sorted = []
        for demande in demandes:
            travaux_sorted = (
                demande.travaux.all()
                .annotate(
                    date_sort=Coalesce(
                        "date", Value("0001-01-01", output_field=DateField())
                    )
                )
                .order_by("-date_sort")
            )
            demandes_travaux_sorted.append((demande, travaux_sorted))

        context['demandes_travaux_sorted'] = demandes_travaux_sorted
        context['form'] = IllustrationForm()

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
    filterset_class = BatiFilterSet
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


class EnquetesDelete(ChildDeleteViewMixin, DeleteView):
    model = Enquetes
    parent_model = Bati


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


class PerspectiveDelete(ChildDeleteViewMixin, DeleteView):
    model = Perspective
    parent_model = Bati


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


class DemandeTravauxDelete(ChildDeleteViewMixin, DeleteView):
    model = DemandeTravaux
    parent_model = Bati


class TravauxCreate(ChildFormViewMixin, CreateView):
    model = Travaux
    parent_model = DemandeTravaux
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Nouveau travaux"

    def dispatch(self, request, *args, **kwargs):
        self.demande = get_object_or_404(DemandeTravaux, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.demande = self.demande
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demande"] = self.demande
        return context

    def get_success_url(self):
        return self.demande.bati.get_detail_url()


class TravauxUpdate(ChildFormViewMixin, UpdateView):
    model = Travaux
    parent_model = Bati
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Modifier les travaux: "


class TravauxDelete(ChildDeleteViewMixin, DeleteView):
    model = Travaux
    parent_model = Bati


class StructureCreate(ChildFormViewMixin, CreateView):
    model = Structure
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Nouvelle structure"
    form_class = StructureForm


class StructureUpdate(ChildFormViewMixin, UpdateView):
    model = Structure
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Modifier la structure"
    form_class = StructureForm


class StructureDelete(ChildDeleteViewMixin, DeleteView):
    model = Structure
    parent_model = Bati


class SecondOeuvreCreate(ChildFormViewMixin, CreateView):
    model = SecondOeuvre
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Nouvelle second oeuvre"
    form_class = SecondOeuvreForm


class SecondOeuvreUpdate(ChildFormViewMixin, UpdateView):
    model = SecondOeuvre
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Modifier la second oeuvre"
    form_class = SecondOeuvreForm


class SecondOeuvreDelete(ChildDeleteViewMixin, DeleteView):
    model = SecondOeuvre
    parent_model = Bati


class StructureFinitionCreate(ChildFormViewMixin, CreateView):
    model = MateriauxFinFinitionStructure
    parent_model = Structure
    parent_related_name = "structure"
    add_label = "Nouvelle finition de structure"
    form_class = MateriauFinFinitionStructureForm

    def dispatch(self, request, *args, **kwargs):
        self.structure = Structure.objects.get(pk=kwargs["structure_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.structure = self.structure
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.structure.get_detail_url()


class StructureFinitionUpdate(ChildFormViewMixin, UpdateView):
    model = MateriauxFinFinitionStructure
    parent_model = Structure
    parent_related_name = "structure"
    add_label = "Modifier la finition de structure"
    form_class = MateriauFinFinitionStructureForm

    def dispatch(self, request, *args, **kwargs):
        self.structure = Structure.objects.get(pk=kwargs["structure_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.structure.get_detail_url()

    def form_valid(self, form):
        form.instance.structure = self.structure
        return super().form_valid(form)


class StructureFinitionDelete(ChildDeleteViewMixin, DeleteView):
    model = MateriauxFinFinitionStructure
    parent_model = Structure


class SecondOeuvreFinitionCreate(ChildFormViewMixin, CreateView):
    model = MateriauxFinFinitionSecondOeuvre
    parent_model = SecondOeuvre
    parent_related_name = "second_oeuvre"
    add_label = "Nouvelle finition de second oeuvre"
    form_class = MateriauFinFinitionSecondOeuvreForm

    def dispatch(self, request, *args, **kwargs):
        self.second_oeuvre = SecondOeuvre.objects.get(pk=kwargs["second_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.second_oeuvre = self.second_oeuvre
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.second_oeuvre.get_detail_url()


class SecondOeuvreFinitionUpdate(ChildFormViewMixin, UpdateView):
    model = MateriauxFinFinitionSecondOeuvre
    parent_model = SecondOeuvre
    parent_related_name = "second_oeuvre"
    add_label = "Modifier la finition de second oeuvre"
    form_class = MateriauFinFinitionSecondOeuvreForm

    def dispatch(self, request, *args, **kwargs):
        self.second_oeuvre = SecondOeuvre.objects.get(pk=kwargs["second_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.second_oeuvre.get_detail_url()

    def form_valid(self, form):
        form.instance.second_oeuvre = self.second_oeuvre
        return super().form_valid(form)


class SecondOeuvreFinitionDelete(ChildDeleteViewMixin, DeleteView):
    model = MateriauxFinFinitionSecondOeuvre
    parent_model = SecondOeuvre

class IllustrationCreateView(CreateView):
    model = Illustration
    form_class = IllustrationForm

    def form_valid(self, form):
        parent = Bati.objects.get(pk=self.kwargs['parent_pk'])
        form.instance.bati = parent
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bati:bati_detail', kwargs={'pk': self.object.bati.pk})

      
from mapentity.views.generic import MapEntityDocumentWeasyprint

class BatiDocumentPdfPublic(MapEntityDocumentWeasyprint):
    model = Bati

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = "bati/bati_public_pdf.html"


class BatiDocumentPdfDetail(MapEntityDocumentWeasyprint):
    model = Bati

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = 'bati/bati_detail_pdf.html'
