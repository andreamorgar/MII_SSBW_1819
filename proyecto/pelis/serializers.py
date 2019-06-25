# pelis/serializers.py
# adaptado para mongoengine

# Aquí podriamos incluir validadores, logs, etc, sobrescribiendo los métodos de la clase para crear, borrar, modificar, listar
# Tarea 12
from rest_framework_mongoengine import serializers
from .models import Pelis

class PelisSerializer(serializers.DocumentSerializer):
	class Meta:
		model = Pelis
		fields = '__all__'
