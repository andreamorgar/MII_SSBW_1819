# from django import forms
from .models import Pelis


from mongodbforms import DocumentForm
from mongodbforms import EmbeddedDocumentForm
from django.forms import TextInput, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class PelisForm(DocumentForm):
    class Meta:
        model = Pelis # nombre del modelo declarado en models.py
        # fields = ('title', 'plot', 'director', 'year', 'runtime')
        fields = ["title","year"]
# widgets = {"title": TextInput(attrs={"size":50,"class":"form-control"}),"rated":TextInput(attrs={"size":50,"class":"form-control"}), "director": TextInput(attrs={"size":50,"class":"form-control"}),"plot": Textarea(attrs={'cols': 50, 'rows': 4,"class":"form-control"}), "poster": TextInput(attrs={"size":50,"class":"form-control"}), "type":TextInput(attrs={"size":50,"class":"form-control"}),"year":NumberInput(attrs={"class":"form-control"}),"runtime":NumberInput(attrs={"class":"form-control"}),"metacritic":NumberInput(attrs={"class":"form-control"})}

class PelisView(DetailView):
    model = Pelis



# class PelisDelete(DeleteView):
#     model = Pelis
#     success_url = reverse_lazy('delete')
