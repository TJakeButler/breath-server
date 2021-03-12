"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from breathapi.models import Journal


class Journals(ViewSet):
    """Types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type
        """
        try:
            journal = Journal.objects.get(pk=pk)
            serializer = JournalSerializer(journal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all types

        Returns:
            Response -- JSON serialized list of game types
        """
        journals = Journal.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = JournalSerializer(
            journals, many=True, context={'request': request})
        return Response(serializer.data)


class JournalSerializer(serializers.ModelSerializer):
    """JSON serializer for journals

    Arguments:
        serializers
    """
    class Meta:
        model = Journal
        fields = ('id', 'entry')       


