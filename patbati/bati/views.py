from ast import Delete
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mapentity.views.generic import (
    MapEntityList, MapEntityDetail,
    MapEntityFormat, MapEntityCreate, MapEntityUpdate, MapEntityDocument,
    MapEntityDelete
)
from mapentity.views.api import MapEntityViewSet
from mapentity.views.mixins import ModelViewMixin
from patbati.bati.forms import DemandeTravauxForm, EnquetesForm, BatiForm, PerspectiveForm, SecondOeuvreFinitionFormSet, SecondOeuvreForm, StructureFinitionFormSet, StructureForm, TravauxForm
from .models import Bati, DemandeTravaux, Enquetes, Perspective, SecondOeuvre, Structure, Travaux
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

    def get_success_url(self):
        return self.object.bati.get_detail_url()

class TravauxCreate(ChildFormViewMixin, CreateView):
    model = Travaux
    parent_model = DemandeTravaux
    form_class = TravauxForm
    parent_related_name = "bati"
    add_label = "Nouveau travaux"

    def dispatch(self, request, *args, **kwargs):
        self.demande = get_object_or_404(DemandeTravaux, pk=kwargs['demande_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.demande = self.demande
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demande'] = self.demande
        return context

    def get_success_url(self):
        return self.demande.bati.get_detail_url()

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

class StructureCreate(ChildFormViewMixin, CreateView):
    model = Structure
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Nouvelle structure"
    form_class = StructureForm

    def dispatch(self, request, *args, **kwargs):
        self.bati = get_object_or_404(Bati, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['finitions_formset'] = StructureFinitionFormSet(self.request.POST, instance=self.object)
        else:
            context['finitions_formset'] = StructureFinitionFormSet(instance=self.object)
        context['bati'] = self.bati
        return context

    def form_valid(self, form):
        form.instance.bati = self.bati
        context = self.get_context_data()
        formset = context['finitions_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.bati.get_detail_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class StructureUpdate(ChildFormViewMixin, UpdateView):
    model = Structure
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Modifier la structure"
    form_class = StructureForm
    pk_url_kwarg = 'structure_pk'

    def dispatch(self, request, *args, **kwargs):
        self.bati = get_object_or_404(Bati, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['finitions_formset'] = StructureFinitionFormSet(self.request.POST, instance=self.object)
        else:
            context['finitions_formset'] = StructureFinitionFormSet(instance=self.object)
        context['bati'] = self.bati
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['finitions_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.bati.get_detail_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class StructureDelete(ChildFormViewMixin, DeleteView):
    model = Structure
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Supprimer la structure"
    template_name = "bati/structure_confirm_delete.html"
    pk_url_kwarg = 'structure_pk'

    def get_success_url(self):
        return self.object.bati.get_detail_url()

class SecondOeuvreCreate(ChildFormViewMixin, CreateView):
    model = SecondOeuvre
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Nouvelle second oeuvre"
    form_class = SecondOeuvreForm

    def dispatch(self, request, *args, **kwargs):
        self.bati = get_object_or_404(Bati, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['finitions_formset'] = SecondOeuvreFinitionFormSet(self.request.POST, instance=self.object)
        else:
            context['finitions_formset'] = SecondOeuvreFinitionFormSet(instance=self.object)
        context['bati'] = self.bati
        return context

    def form_valid(self, form):
        form.instance.bati = self.bati
        context = self.get_context_data()
        formset = context['finitions_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.bati.get_detail_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SecondOeuvreUpdate(ChildFormViewMixin, UpdateView):
    model = SecondOeuvre
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Modifier la second oeuvre"
    form_class = SecondOeuvreForm
    pk_url_kwarg = 'second_pk'

    def dispatch(self, request, *args, **kwargs):
        self.bati = get_object_or_404(Bati, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['finitions_formset'] = SecondOeuvreFinitionFormSet(self.request.POST, instance=self.object)
        else:
            context['finitions_formset'] = SecondOeuvreFinitionFormSet(instance=self.object)
        context['bati'] = self.bati
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['finitions_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.bati.get_detail_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SecondOeuvreDelete(ChildFormViewMixin, DeleteView):
    model = SecondOeuvre
    parent_model = Bati
    parent_related_name = "bati"
    add_label = "Supprimer la second oeuvre"
    template_name = "bati/second_confirm_delete.html"
    pk_url_kwarg = 'second_pk'

    def get_success_url(self):
        return self.object.bati.get_detail_url()

    