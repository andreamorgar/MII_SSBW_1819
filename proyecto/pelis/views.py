from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect

# from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.urls import reverse
from .models import Pelis
import re

# tarea 9
from django.contrib.auth.decorators import login_required
# Create your views here.

# ------------------------------------------------------------------------------
def prueba_mongoengine(request):
    salida = '''<html>
                    ¡Hola mundo en el proyecto pelis!
                </html>
                '''
    return HttpResponse(salida)
# ------------------------------------------------------------------------------
def info_de(request,id):
    print("-------------------> ID: "+id)
    peli = Pelis.objects().get(id=id)
    print("Director: " + str(peli.title))

    # salida = '''<html>
    #                 Titulo: %s
    #             </html>
    #             ''' % (str(peli.title))
    #
    # return HttpResponse(salida)

    context = {
        'id':id,
        'peli': Pelis.objects().get(id=id)
    }
    return render(request,"pelis/info_de.html",context)
# ------------------------------------------------------------------------------
def consulta_por_genero(request,genero):
    print("-------------------> Genero: "+genero)

    # context = {
    #     'lista': Pelis.objects(genero=genero)[:10],
    #     'genero': genero
    # }
    # return render(request,"salida_consulta.html",request)


    pelis = Pelis.objects().get(genres=genero)
    peli = pelis[0]
    print("Director: " + peli.director)

    salida = '''<html>
                    Director: %s
                </html>
                ''' % (str(peli.director))

    return HttpResponse(salida)

# ------------------------------------------------------------------------------
def consulta_por_peli(request,id):
    print("-------------------> Peli buscada: "+id)

    peli = Pelis.objects().get(id=id)

    url_imagen = peli['poster']
    nominaciones = ""
    votos_imdb = ""
    galardones = ""

    if peli['awards']['wins'] is not None:
        galardones = int(peli['awards']['wins'])

    if peli['awards']['nominations'] is not None:
        nominaciones = int(peli['awards']['nominations'])

    if peli['imdb']['votes'] is not None:
        votos_imdb = int(peli['imdb']['votes'])

    if url_imagen is not None:
        context = {
            'peli':  peli,
            'galardones': galardones,
            'nominaciones': nominaciones,
            'votos_imdb': votos_imdb,
            'url_imagen': url_imagen[0:4]+'s'+url_imagen[4:]

        }

    else:
        context = {
            'peli':  peli,
            'galardones': galardones,
            'nominaciones': nominaciones,
            'votos_imdb': votos_imdb,

        }
    # context = {
    #     'titulo':  peli.title,
    #     'genero': peli.genres,
    #
    # }

    return render(request,"pelis/pelicula.html",context)


    # peli = Pelis.objects().get(title=title)
    # print("Nombre: " + peli.title)
    #
    # salida = '''<html>
    #                 Título: %s
    #             </html>
    #             ''' % (str(peli.title))
    #
    # return HttpResponse(salida)

# ------------------------------------------------------------------------------
def busqueda_pelis(request):
    context = {}
    lista = []

    # obtener géneros
    lista_pelis = Pelis.objects()

    generos = []
    for pelicula in lista_pelis:
        for genero in pelicula["genres"]:
            generos.append(genero)

    set_generos = set(generos)

    if(request.method == 'POST'):
        actor_formulario = request.POST.get('var_actor')

        # La primera letra de actor tiene que estar en mayúscula para que la búsqueda sea correcta
        actor_formulario = actor_formulario[0].upper() + actor_formulario[1:]
        year_formulario = request.POST.get('var_year')
        genero_formulario = request.POST.get('var_genres')
        print(genero_formulario)

        if actor_formulario != "" and year_formulario != "" and genero_formulario != "Seleccionar":
            lista = Pelis.objects().filter(genres__contains = genero_formulario, year = int(year_formulario), actors__contains = actor_formulario)
            print(lista)
        elif genero_formulario != "Seleccionar":

            if year_formulario != "":
                lista = Pelis.objects().filter(genres__contains = genero_formulario, year = int(year_formulario))
                # lista = pelis.find({"year":int(year_formulario),"genres": regx_genres})
            elif actor_formulario != "":
                lista = Pelis.objects().filter(genres__contains = genero_formulario, actors__contains = actor_formulario)
                # lista = pelis.find({"actors": regx,"genres": regx_genres})

        else:
            if year_formulario != "":
                # lista = pelis.find({"year":int(year_formulario)})
                lista = Pelis.objects().filter(year = int(year_formulario))
            elif actor_formulario != "":
                lista = Pelis.objects().filter(actors__contains = actor_formulario)
                # lista = pelis.find({"actors": regx})
            else:
                lista = []

        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])

        context = {
            'value_genero':genero_formulario,
            'value_actor': actor_formulario,
            'value_year':year_formulario,
            'lista': lista_aux,
            'generos': list(set_generos),
        }


    else:
        lista = Pelis.objects()
        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])


        context = {
            'lista': lista_aux,
            'generos': list(set_generos),
        }


    return render(request,"pelis/main.html",context)

# # ----------------------------------------------------------------------------
# # tarea 7 ------->  https://tutorial.djangogirls.org/es/django_forms/
# ------------------------------------------------------------------------------

from .forms import PelisForm

@login_required(login_url='/accounts/login/')
def post_new(request):
    # form = PelisForm()
    # print("hola")
    # return render(request, 'pelis/post_edit.html', {'form': form})
    #https://medium.com/@siddharthshringi/how-i-made-my-first-django-app-4ede65c9b17f
    if request.method == 'POST':
        form = PelisForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('/pelis/tarea7/vista_crud')
            return HttpResponseRedirect(reverse('vamo'))
    else:
        form = PelisForm()

    return render(request, 'pelis/post_edit.html', {'form': form})


# https://rayed.com/posts/2018/05/django-crud-create-retrieve-update-delete/
@login_required
def editar_peli(request, id, template_name='pelis/post_edit.html'):
    peli = Pelis.objects().get(id=id)
    form = PelisForm(request.POST or None, instance=peli)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('vamo'))
    return render(request, template_name, {'form':form})


# https://rayed.com/posts/2018/05/django-crud-create-retrieve-update-delete/
@login_required
def borrar_peli(request, id, template_name='pelis/film_confirm_delete.html'):

    peli = Pelis.objects().get(id=id)
    # peli = get_object_or_404(Pelis, id=id)

    if request.method=='POST':
        peli.delete()
        return HttpResponseRedirect(reverse('vamo'))

    return render(request, template_name, {'object':peli})





# ------------------------------------------------------------------------------
def vista_crud(request):
    context = {}
    lista = []

    # print(request.user.is_authenticated)
    # Para poner el botón de Login o Logout tenemos que saber antes si está el
    # usuario logeado o no
    user_autenticado = "no"
    if request.user.is_authenticated:
        user_autenticado = "yes"

    # obtener géneros
    lista_pelis = Pelis.objects()

    generos = []
    for pelicula in lista_pelis:
        for genero in pelicula["genres"]:
            generos.append(genero)

    set_generos = set(generos)

    if(request.method == 'POST'):
        actor_formulario = request.POST.get('var_actor')
        year_formulario = request.POST.get('var_year')
        genero_formulario = request.POST.get('var_genres')
        print(genero_formulario)


        if actor_formulario != "" and year_formulario != "" and genero_formulario != "Seleccionar":
            # La primera letra de actor tiene que estar en mayúscula para que la búsqueda sea correcta
            actor_formulario = actor_formulario[0].upper() + actor_formulario[1:]
            lista = Pelis.objects().filter(genres__contains = genero_formulario, year = int(year_formulario), actors__contains = actor_formulario)
            print(lista)
        elif genero_formulario != "Seleccionar":

            if year_formulario != "":
                lista = Pelis.objects().filter(genres__contains = genero_formulario, year = int(year_formulario))
                # lista = pelis.find({"year":int(year_formulario),"genres": regx_genres})
            elif actor_formulario != "":
                # La primera letra de actor tiene que estar en mayúscula para que la búsqueda sea correcta
                actor_formulario = actor_formulario[0].upper() + actor_formulario[1:]
                lista = Pelis.objects().filter(genres__contains = genero_formulario, actors__contains = actor_formulario)
                # lista = pelis.find({"actors": regx,"genres": regx_genres})
            else:
                print("entra aqui jeje")
                lista = Pelis.objects().filter(genres__contains = genero_formulario)

        else:
            if year_formulario != "":
                # lista = pelis.find({"year":int(year_formulario)})
                lista = Pelis.objects().filter(year = year_formulario)
            elif actor_formulario != "":
                lista = Pelis.objects().filter(actors__contains = actor_formulario)
                # lista = pelis.find({"actors": regx})
            else:
                lista = []


        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])

        context = {
            'value_genero':genero_formulario,
            'value_actor': actor_formulario,
            'value_year':year_formulario,
            'lista': lista_aux,
            'generos': list(set_generos),
            'user_autenticado':user_autenticado,
        }


    else:
        lista = Pelis.objects()
        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])


        context = {
            'lista': lista_aux,
            'generos': list(set_generos),
            'user_autenticado':user_autenticado,
        }


    return render(request,"pelis/mainCrud.html",context)


# ==============================================================================
# ==============================================================================
# TAREA 12
# ==============================================================================
# ==============================================================================


# ------------------------------------------------------------------------------
# API desde funciones
# ------------------------------------------------------------------------------

from django.http import JsonResponse
from .serializers import PelisSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

# Listar todas, Añadir
# Note that because we want to be able to POST to this view from clients t
# hat won't have a CSRF token we need to mark the view as csrf_exempt.
# This isn't something that you'd normally want to do, and REST framework
# views actually use more sensible behavior than this, but it'll do for
# our purposes right now.
# https://www.django-rest-framework.org/tutorial/1-serialization/#introduction
@csrf_exempt
def api_pelis(request):
	if request.method == 'GET':
		pelis_ = Pelis.objects.all()[:10]
		serializer = PelisSerializer(pelis_, many=True)
		return JsonResponse(serializer.data, safe=False)

    # Este no lo he comprobado
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = PelisSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)

	logger.debug('Error')
	return JsonResponse(serializers.errors, stauts=400)


# Para el post, he usado postman: https://www.toolsqa.com/postman/post-request-in-postman/
# Introducimos en Raw -> Json el siguiente:
# {"title": "South Side Story", "year": 1960, "rated": "UNRATED", "runtime": 152, "countries": ["USA"], "genres": ["Crime", "Drama", "Musical"], "director": "Jerome Robbins, Robert Wise", "writers": ["Ernest Lehman", "Arthur Laurents", "Jerome Robbins"], "actors": ["Natalie Wood", "Richard Beymer", "Russ Tamblyn", "Rita Moreno"], "plot": "Two youngsters from rival New York City gangs fall in love, but tensions between their respective friends build toward tragedy.", "poster": "http://ia.media-imdb.com/images/M/MV5BMTM0NDAxOTI5MF5BMl5BanBnXkFtZTcwNjI4Mjg3NA@@._V1_SX300.jpg", "imdb": {"id": "tt0055614", "rating": 7.6, "votes": 67824.0}, "tomato": {}, "metacritic": 2, "awards": {"wins": 18.0, "nominations": 11.0, "text": "Won 10 Oscars. Another 18 wins & 11 nominations."}, "type": "movie"}
# Luego se comprueba, y funciona bien, porque la respuesta es el mismo json pero
# ya almacenado

# ------------------------------------------------------------------------------
# Listar, Modificar, Borrar
@csrf_exempt
def api_peli(request, id):
    try:
        peli = Pelis.objects().get(id=id)
    except:
        logger.debug('Peli no encontrada '+id)
        return HttpResponse(status=404)  # No encontrado

    if request.method == 'GET':
        # http://localhost:8000/pelis/tarea12/api_peli/5b107bec1d2952d0da9046e3
        serializer = PelisSerializer(peli)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        # {"title": "SS Camp 5: Women's Heaven", "year": 1977, "rated": "UNRATED", "runtime": 96, "countries": ["Italy"], "genres": ["Drama", "Thriller", "War"], "director": "Sergio Garrone", "writers": ["Sergio Garrone", "Vinicio Marinucci", "Tecla Romanelli"], "actors": ["Paola Corazzi", "Rita Manna", "Giorgio Cerioni", "Serafino Profumo"], "plot": "During the last days of WW2, several female prisoners arrive at Camp 5 to work as sex slaves for officers and guinea pigs for horrific experiments by Nazi doctors who are trying to find a ...", "poster": "http://ia.media-imdb.com/images/M/MV5BMTk5NjY3MzExN15BMl5BanBnXkFtZTcwODI1NzgxMw@@._V1_SX300.jpg", "imdb": {"id": "tt0147310", "rating": 4.3, "votes": 428.0}, "tomato": {}, "metacritic": 2, "awards": {"wins": 0.0, "nominations": 0.0, "text": ""}, "type": "movie"}


        # para saber qué status poner: https://www.restapitutorial.com/lessons/httpmethods.html
        data = JSONParser().parse(request)
        # Tenemos que tener cuidado, porque con PUT queremos modificar un recurso
        # ya existente, así que tenemos que pasarle el ID
        serializer = PelisSerializer(peli,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

    if request.method == 'DELETE':
        # http://localhost:8000/pelis/tarea12/api_peli/5d11ce465002cb5369f78dfc
        # eliminamos la peli con el ID recibido como parámetro con el delete
        peli.delete()
        #podemos devolver 200 o 404: https://www.restapitutorial.com/lessons/httpmethods.html
        return HttpResponse(status=200)





# ------------------------------------------------------------------------------
#  APIS desde clases viewsets
# ------------------------------------------------------------------------------
