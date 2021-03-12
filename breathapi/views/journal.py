"""View module for handling requests about journals"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from breathapi.models import Journal
from breathapi.models import Log
from django.core.exceptions import ValidationError
from rest_framework import status


class Journals(ViewSet):
    """Journals"""
    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized event instance
        """
        

        journal = Journal()
        journal.entry = request.data["entry"]

        # log = Log.objects.get(pk=request.data["log_id"])
        # journal.log = log

        try:
            journal.save()
            serializer = JournalSerializer(journal, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

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

class LogSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializers
    """
    class Meta:
        model = Log
        fields = ('id', 'user', 'type', 'journal', 'date', 'time')       

    


