"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from breathapi.models import Type


class Types(ViewSet):
    """Types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type
        """
        try:
            type = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all types

        Returns:
            Response -- JSON serialized list of game types
        """
        types = Type.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TypeSerializer(
            types, many=True, context={'request': request})
        return Response(serializer.data)


class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for types

    Arguments:
        serializers
    """
    class Meta:
        model = Type
        fields = ('id', 'name', 'inhale', 'exhale', 'hold')       


