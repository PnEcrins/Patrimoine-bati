from django.db import models


class ChildFormViewMixin:
    """
    Mixin for separate child form
    Manage :
    - add child form to parent
    - Add information to context to use mapentity layout (navbar)
    - fetch parent object and add the child form to it

    """

    view_name = "add"
    # model of the parent of form
    parent_model = None
    # label use to the title of form "New" <model> for <oject>
    add_label = "Nouveau"
    template_name = "child_form.html"

    def get_parent_model(self):
        return self.parent_model

    def dispatch(self, request, *args, **kwargs):
        self.parent_object = self.parent_model.objects.get(pk=kwargs["parent_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viewname"] = self.view_name
        context["title"] = self.parent_object
        context["add_label"] = self.add_label
        parent_model = self.get_parent_model()

        if parent_model and self.model:
            context["date_fields"] = [field.name for field in self.model._meta.fields if isinstance(field, models.DateField)]
            context["model"] = parent_model
            context["appname"] = parent_model._meta.app_label.lower()
            context["app_verbose_name"] = parent_model._meta.app_config.verbose_name
            context["modelname"] = self.model._meta.object_name.lower()
        return context

    def form_valid(self, form):
        setattr(form.instance, self.parent_related_name, self.parent_object)
        return super().form_valid(form)

    def get_success_url(self):
        return self.parent_object.get_detail_url()


class ChildDeleteViewMixin:
    parent_model = None

    def get_template_names(self):
        return super().get_template_names() + [
            "mapentity/mapentity_confirm_delete.html"
        ]

    def dispatch(self, request, *args, **kwargs):
        self.parent_object = self.parent_model.objects.get(pk=kwargs["parent_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.parent_object.get_detail_url()
