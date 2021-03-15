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
    def update(self, request, pk=None):
            """Handle PUT requests for a log

            Returns:
                Response -- Empty body with 204 status code
            """
            # gamer = Gamer.objects.get(user=request.auth.user)

            # Do mostly the same thing as POST, but instead of
            # creating a new instance of Game, get the game record
            # from the database whose primary key is `pk`
            journal = Journal.objects.get(pk=pk)
            journal.entry = request.data["entry"]

            journal.save()
            

            # log = Log.objects.get(pk=request.data["gameTypeId"])
            # game.gametype = gametype
            # game.save()

            # 204 status code means everything worked but the
            # server is not sending back any data in the response
            return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            journal = Journal.objects.get(pk=pk)
            journal.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Journal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    


