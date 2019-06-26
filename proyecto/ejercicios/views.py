from django.shortcuts import render
from django.shortcuts import HttpResponse

import random
import re
from requests import *

def hola_mundo_basico(request):
    salida = '''<html>
                    Hola mundo
                </html>
                '''
    return HttpResponse(salida)


def hola_mundo(request,usuario):
    salida = '''<html>
                    Hola %s
                </html>
                ''' % (usuario)

    return HttpResponse(salida)

#pasamos lista con elementos separados por espacio
def ejercicio_1(request,lista):
    lista_string = lista.split()
    count = 0
    for i in lista_string:
        if len(i) >= 2 and i[0] == i[-1]:
            count += 1

    salida = '''<html>
                    Recuento: %s
                </html>
                ''' % (str(count))

    return HttpResponse(salida)




def ejercicio_2(request,lista):

    lista_string = lista.split()
    myset = set(lista_string)

    salida = '''<html>
                    %s
                </html>
                ''' % (myset)


    return HttpResponse(salida)



def ejercicio_3(request,entrada):
    var = ""
    if len(entrada) < 2:
        var = entrada
    else:
        var = entrada[0:2] + entrada[len(entrada)-2:]

    salida = '''<html>
                    %s
                </html>
                ''' % (var)

    return HttpResponse(salida)



def ejercicio_4(request,string):

    var = string

    if len(string) > 2:
        if  string[len(string)-3:] == "ing":
            var = string + "ly"
        else:
            var = string + "ing"


    salida = '''<html>
                    %s
                </html>
                ''' % (var)

    return HttpResponse(salida)




def ejercicio_5(request):

    text = """ Read any text file specified on the command line.
    Do a simple split() on whitespace to obtain all the words in the file.
    Rather than read the file line by line, it's easier to read
    it into one giant string and split it once.

    Build a "mimic" dict that maps each word that appears in the file
    to a list of all the words that immediately follow that word in the file.
    The list of words can be be in any order and should include
    duplicates. So for example the key "and" might have the list
    ["then", "best", "then", "after", ...] listing
    all the words which came after "and" in the text.
    We'll say that the empty string is what comes before
    the first word in the file.

    With the mimic dict, it's fairly easy to emit random
    text that mimics the original. Print a word, then look
    up what words might come next and pick one at random as
    the next work.
    Use the empty string as the first word to prime things.
    If we ever get stuck with a word that is not in the dict,
    go back to the empty string to keep things moving.

    Note: the standard python module 'random' includes a
    random.choice(list) method which picks a random element
    from a non-empty list.

    For fun, feed your program to itself as input.
    Could work on getting it to put in linebreaks around 70
    columns, so the output looks better."""

    text = re.sub('[^a-zA-Z0-9_]', ' ', text)
    # text = text.replace([".",","], "")

    words = text.split()

    # Obtenemos el diccionario
    # Clave: palabra del texto
    # Valor: lista con todas las palabras que siguen cada aparición
    # de la palabra que, en este caso, es la clave.

    mydict = {}
    for i,word in enumerate(words):

        if word in mydict.keys():
            if i < len(words)-1:
                mydict[word].append(words[i+1])
        else:
            if i < len(words)-1:
                mydict[word] = [words[i+1]]

    var = words[0]

    for key in mydict.keys():
        element = ""
        if len(mydict[key]) > 1:
            element =  mydict[key][random.randint(0,len(mydict[key])-1)]
            var = var + " " + element.lower()
        else:
            var = var + " " + mydict[key][0].lower()
    var += "."

    salida = '''<html>
                    %s
                </html>
                ''' % (var)
    return HttpResponse(salida)




def ejercicio_templates(request):
    context = {
    'año': 2019,
    'lista': [ {'nombre':'pepe', 'numero':2},
    {'nombre':'juan', 'numero':28},
    ]

    }

    return render(request, 'ejercicios/nombres.html', context)


import requests as requests

from requests.packages.urllib3.util.retry import Retry
retry = Retry(connect=3, backoff_factor=0.5)
# from xml.etree import ElementTree



import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def titulares(request):
    url = 'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
    response = requests.get(url)

    # tree = ElementTree.fromstring(response.content)
    texto = response.content
    res = re.findall(r'<title><!\[CDATA\[(.+?)\]\]><\/title>', response.text)
    # print(str(res))
    # print(type(res))
    # print("Numero titulares: "+ str(len(res)))


    # salida = '''<html>
    #                 blabla
    #             </html>
    #             '''
    # return HttpResponse(salida)

    context = {
    'titulo':res[0],
    'lista': res[1:] # los dos primeros no son info de titulares
    }
    return render(request, 'ejercicios/titulares.html', context)


def portada(request):
    url = 'http://ep00.epimg.net/rss/tecnologia/portada.xml'
    response = requests.get(url)

    # Primero obtenemos los titulares, de igual forma que antes
    texto = response.content
    titulares_ = re.findall(r'<title><!\[CDATA\[(.+?)\]\]><\/title>', response.text)
    print("Numero titulares: "+ str(len(titulares_)))

    imagenes_ = re.findall(r'<enclosure url="(.+?)"', response.text)
    # print("Numero de imágenes: "+ str(len(imagenes_)))

    # salida = '''<html>
    #                 blabla
    #             </html>
    #             '''
    # return HttpResponse(salida)

    # context = {
    # 'titulo':titulares_[0],
    # 'lista': titulares_[1:] ,# los dos primeros no son info de titulares
    # 'imagenes': imagenes_,
    # }

    info = []
    seq = [1,3,5,7,9,11,13,15,17,19]
    for i in range(0,10):
        list_info = {}
        list_info['titular'] = titulares_[1+i]
        list_info['img'] = imagenes_[seq[i]]
        # print(str(i+2-1))
        info.append(list_info)
        # info[titulares[1+i]] = imagenes_[(i+2)-1]

    context = {
    'titulo':titulares_[0],
    'info':info,
    # 'lista': titulares_[1:] ,# los dos primeros no son info de titulares
    # 'imagenes': imagenes_,
    }
    return render(request, 'ejercicios/titulares.html', context)



from pymongo import *
client = MongoClient('mongo',27017)
db = client.movies
pelis = db.pelis

def pymongo(request):
    lista = []
    lista = pelis.find({}).limit(10)
    print(pelis.count_documents({}))
    # print("hola")
    # print(lista)
    # for doc in lista:
    #     print(doc)
    context = {
        'lista': lista
    }
    return render(request,"ejercicios/salida.html",context)


def get_pelis_pymongo(request,year):
    # busqueda = ".*"+ request.actor + ".*"
    # lista = pelis.find({"actors" : {$regex : }});
    lista = pelis.find({"year":int(year)})


    context = {
        'lista': lista
    }


    return render(request,"ejercicios/table.html",context)


def busqueda_pelis(request):
    context = {}
    lista = []

    # obtener géneros
    lista_pelis = pelis.find({})

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
    #     if actor_formulario != "" and year_formulario != "":
    #         regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
    #         lista = pelis.find({"actors": regx, "year":int(year_formulario)})
    #     elif year_formulario != "":
    #         lista = pelis.find({"year":int(year_formulario)})
    #     elif actor_formulario != "":
    #         regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
    #         lista = pelis.find({"actors": regx})
    #     else:
    #         # lista = pelis.find()
    #         lista = []
    #

        if actor_formulario != "" and year_formulario != "" and genero_formulario != "Seleccionar":
            regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
            regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
            lista = pelis.find({"actors": regx, "year":int(year_formulario),"genres": regx_genres})
        elif genero_formulario != "Seleccionar":
            regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
            if year_formulario != "":
                lista = pelis.find({"year":int(year_formulario),"genres": regx_genres})
            elif actor_formulario != "":
                regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
                lista = pelis.find({"actors": regx,"genres": regx_genres})
            else:
                regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
        else:
            if year_formulario != "":
                lista = pelis.find({"year":int(year_formulario)})
            elif actor_formulario != "":
                regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
                lista = pelis.find({"actors": regx})
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
        lista = pelis.find()
        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])


        context = {
            'lista': lista_aux,
            'generos': list(set_generos),
        }



    return render(request,"ejercicios/main.html",context)





def busqueda_pelis_css(request):
    context = {}
    lista = []

    # obtener géneros
    lista_pelis = pelis.find({})

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
    #     if actor_formulario != "" and year_formulario != "":
    #         regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
    #         lista = pelis.find({"actors": regx, "year":int(year_formulario)})
    #     elif year_formulario != "":
    #         lista = pelis.find({"year":int(year_formulario)})
    #     elif actor_formulario != "":
    #         regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
    #         lista = pelis.find({"actors": regx})
    #     else:
    #         # lista = pelis.find()
    #         lista = []
    #

        if actor_formulario != "" and year_formulario != "" and genero_formulario != "Seleccionar":
            regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
            regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
            lista = pelis.find({"actors": regx, "year":int(year_formulario),"genres": regx_genres})
        elif genero_formulario != "Seleccionar":
            regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
            if year_formulario != "":
                lista = pelis.find({"year":int(year_formulario),"genres": regx_genres})
            elif actor_formulario != "":
                regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
                lista = pelis.find({"actors": regx,"genres": regx_genres})
            else:
                regx_genres = re.compile("^"+ genero_formulario, re.IGNORECASE)
        else:
            if year_formulario != "":
                lista = pelis.find({"year":int(year_formulario)})
            elif actor_formulario != "":
                regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
                lista = pelis.find({"actors": regx})
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
        lista = pelis.find()
        # necesario para quitar el float del año
        lista_aux = [i for i in lista]
        for i,peli in enumerate(lista_aux):
            lista_aux[i]['year'] = int(peli['year'])


        context = {
            'lista': lista_aux,
            'generos': list(set_generos),
        }



    return render(request,"ejercicios/main_c.html",context)
