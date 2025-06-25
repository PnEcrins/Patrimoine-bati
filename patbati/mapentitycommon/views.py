from django.shortcuts import render

class ChildFormViewViewMixin:
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

    def get_parent_model(self):
        return self.parent_model
    
    def dispatch(self, request, *args, **kwargs):
        self.parent_object = self.parent_model.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewname'] = self.view_name
        context['title'] = self.parent_object

        parent_model = self.get_parent_model()

        if parent_model:
            context['model'] = parent_model
            context['appname'] = parent_model._meta.app_label.lower()
            context['app_verbose_name'] = parent_model._meta.app_config.verbose_name
            context['modelname'] = parent_model._meta.object_name.lower()
            context['objectname'] = parent_model._meta.verbose_name
            context['objectsname'] = parent_model._meta.verbose_name_plural
        return context
    
    def form_valid(self, form):
        setattr(form.instance, self.parent_related_name, self.parent_object)
        return super().form_valid(form)

    def get_success_url(self):
        return self.parent_object.get_detail_url()