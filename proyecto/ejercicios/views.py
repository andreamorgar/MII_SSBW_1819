from django.shortcuts import render
from django.shortcuts import HttpResponse

import random
import re
from requests import *
# import requests


# def hola_mundo(request):
#     salida = '''<html>
#                     Hola mundo
#                 </html>
#                 '''
#     return HttpResponse(salida)


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

    return render(request, 'nombres.html', context)


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
    print(re.findall(r'<title><!\[CDATA\[(.+?)\]\]><\/title>', response.text))


    salida = '''<html>
                    blabla
                </html>
                '''

    return HttpResponse(salida)


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
    return render(request,"salida.html",context)


def get_pelis_pymongo(request,actor):
    # busqueda = ".*"+ request.actor + ".*"
    # lista = pelis.find({"actors" : {$regex : }});
    lista = pelis.find({"year":int(actor)})


    context = {
        'lista': lista
    }


    return render(request,"table.html",context)


def busqueda_pelis(request):
    lista = []

    # lista = pelis.find({"year":int(actor)})
    #
    #
    # context = {
    #     'lista': lista
    # }
    if(request.method == 'POST'):
        actor_formulario = request.POST.get('var_actor')
        # print(x)
        year_formulario = request.POST.get('var_year')

        if actor_formulario == "":
            lista = pelis.find({"year":int(year_formulario)})
        elif year_formulario == "":
            regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
            lista = pelis.find({"actors": regx})
        else:
            regx = re.compile("^"+ actor_formulario, re.IGNORECASE)
            lista = pelis.find({"actors": regx, "year":int(year_formulario)})

        context = {
            'lista': lista
        }

        # if len(lista) == 0:
        #     return render(request,"no_result.html")

        return render(request,"table.html",context)

    else:
        return render(request,"formulario.html")
