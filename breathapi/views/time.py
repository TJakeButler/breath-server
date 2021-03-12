"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from breathapi.models import Time


class Times(ViewSet):
    """Types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type
        """
        try:
            time = Time.objects.get(pk=pk)
            serializer = TimeSerializer(time, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all types

        Returns:
            Response -- JSON serialized list of game types
        """
        times = Time.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TimeSerializer(
            times, many=True, context={'request': request})
        return Response(serializer.data)


class TimeSerializer(serializers.ModelSerializer):
    """JSON serializer for times

    Arguments:
        serializers
    """
    class Meta:
        model = Time
        fields = ('id', 'minutes')       


