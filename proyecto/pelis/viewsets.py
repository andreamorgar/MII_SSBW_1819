# pelis/viewsets.py
from rest_framework_mongoengine import viewsets
from .models import Pelis
from .serializers import PelisSerializer

class PelisViewSet(viewsets.ModelViewSet):
    queryset = Pelis.objects.all()[:10]
    lookup_field = 'id'
    serializer_class = PelisSerializer


    # Aquí también podriamos sobreescribir los métodos, de leer, añadir, borrar, etc
