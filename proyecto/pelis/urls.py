from django.urls import path
from . import views

from django.conf.urls import include, url
from rest_framework import routers
from .viewsets import PelisViewSet

router = routers.DefaultRouter()
router.register('pelis', PelisViewSet, 'peli')

urlpatterns = [
    path('tarea4/prueba_mongoengine', views.prueba_mongoengine),   # entrada str
    path('genero/<genero>',views.consulta_por_genero),
    path('id/<id>',views.info_de,name="info_de"),
    path('tarea5/pelicula/<id>',views.consulta_por_peli),
    path('tarea5/busqueda', views.busqueda_pelis),

    path('tarea7/vista_crud', views.vista_crud, name='vamo'),
    path('tarea7/post_new', views.post_new, name='create'),

    # https://rayed.com/posts/2018/05/django-crud-create-retrieve-update-delete/
    path('tarea7/ver/<id>', views.consulta_por_peli, name='read'),
    path('tarea7/editar/<id>', views.editar_peli, name='edit'),
    path('tarea7/borrar/<id>', views.borrar_peli, name='delete'),


    # Tarea 12
    path('tarea12/api_pelis',    views.api_pelis),  # GET lista todas, POST añade
    path('tarea12/api_peli/<id>', views.api_peli),  # GET lista una,   PUT modifica, DELETE borrra

    url('api', include(router.urls)), # Incluye todo el API CRUD -> http://localhost:8000/pelis/apipelis/
	]
