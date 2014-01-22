# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views import generic

from ..bts import models
from . import forms


class BaseStationPanelView(generic.UpdateView):
    template_name = 'panel/basestation.html'
    model = models.BaseStation
    form_class = forms.BaseStationEditForm
    context_object_name = 'base_station'

    def get_object(self, queryset=None):
        """
        When creating a new object, return None which tells generic Django
        the view should emulate generic.CreateView.
        Inspiration taken from:
        https://github.com/tangentlabs/django-oscar/blob/master/oscar/apps/dashboard/catalogue/views.py#L188
        """
        self.creating = not 'pk' in self.kwargs
        if self.creating:
            return None
        return super(BaseStationPanelView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(BaseStationPanelView, self).get_context_data(**kwargs)
        if not self.creating:
            ctx['cell_formset'] = forms.BaseStationCellsFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        if not self.creating:
            # If not creating a new BaseStation record, validate the formset
            cell_formset = forms.BaseStationCellsFormSet(self.request.POST,
                                                         instance=self.object)
            if not cell_formset.is_valid():
                return self.form_invalid(form)
            cell_formset.save()

        return super(BaseStationPanelView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Formularz zawiera błędy')
        return super(BaseStationPanelView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'Rekord zachowano poprawnie')
        return reverse('panel:basestation-edit-view', kwargs={'pk': self.object.id})
