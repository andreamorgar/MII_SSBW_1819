from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('tarea1/hola_mundo', views.hola_mundo_basico),	# entrada str
    path('tarea1/<usuario>', views.hola_mundo),	# entrada str

    path('tarea2/1/<lista>', views.ejercicio_1),   # entrada str, lista separada por espacios
    path('tarea2/2/<lista>', views.ejercicio_2),   # entrada str, lista separada por espacios
    path('tarea2/3/<entrada>', views.ejercicio_3), # entrada str
    path('tarea2/4/<string>', views.ejercicio_4),  # entrada str
    path('tarea2/5/', views.ejercicio_5), # entrada str

    path('ejercicio_templates/', views.ejercicio_templates), # entrada str
    path('tarea3/noticias/titulares', views.titulares),
	path('tarea3/noticias/portada', views.portada),


    path('ejercicio_pymongo/', views.pymongo), # entrada str
    path('tarea5/actores_pymongo/<actor>', views.get_pelis_pymongo), # entrada str
    path('tarea5/busqueda', views.busqueda_pelis), # entrada str

	]
