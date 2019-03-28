from django.urls import path

from . import views

urlpatterns = [
	# path('hola_mundo', views.hola_mundo),	# entrada str
    # path('<usuario>', views.hola_mundo),	# entrada str
    path('1/<lista>', views.ejercicio_1),   # entrada str, lista separada por espacios
    path('2/<lista>', views.ejercicio_2),   # entrada str, lista separada por espacios
    path('3/<entrada>', views.ejercicio_3), # entrada str
    path('4/<string>', views.ejercicio_4),  # entrada str
    path('5/', views.ejercicio_5), # entrada str

    path('ejercicio_templates/', views.ejercicio_templates), # entrada str
    path('noticias/titulares', views.titulares),
    path('ejercicio_pymongo/', views.pymongo), # entrada str
    path('tarea5/actores_pymongo/<actor>', views.get_pelis_pymongo), # entrada str
    path('tarea5/busqueda', views.busqueda_pelis), # entrada str

	]
