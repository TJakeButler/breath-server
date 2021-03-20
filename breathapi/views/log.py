"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from breathapi.models import Log
from breathapi.models import Type
from breathapi.models import Time
from django.contrib.auth.models import User


class Logs(ViewSet):
    """Level up logs"""


    def destroy(self, request, pk=None):

            try:
                log = Log.objects.get(pk=pk)
                log.delete()

                return Response({}, status = status.HTTP_204_NO_CONTENT)

            except Log.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status = status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle Put operations for logs

        Returns:
            Response -- JSON serialized event instance
        """
        log = Log.objects.get(pk=pk)
        log.user = request.auth.user

        # if request.data["journal"] is not None:
        #     journal = Journal.objects.get(pk=request.data["journal"])
        #     log.journal = journal

        log.date = log.date
        log.journal = request.data["journal"]
        time = Time.objects.get(pk=request.data["time"])
        log.time = time
        type = Type.objects.get(pk=request.data["type"])
        log.type = type
        # log = Log.objects.get(pk=request.data["log_id"])
        # journal.log = log

        
        log.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

        #     serializer = LogSerializer(log, context={'request': request})
        #     return Response(serializer.data)
        # except ValidationError as ex:
        #     return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized event instance
        """
        log = Log()
        log.user = request.auth.user

        # if request.data["journal"] is not None:
        #     journal = Journal.objects.get(pk=request.data["journal"])
        #     log.journal = journal

        log.date = request.data["date"]
        log.journal = request.data["journal"]
        time = Time.objects.get(pk=request.data["time"])
        log.time = time
        type = Type.objects.get(pk=request.data["type"])
        log.type = type
        # log = Log.objects.get(pk=request.data["log_id"])
        # journal.log = log

        try:
            log.save()
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to logs resource

        Returns:
            Response -- JSON serialized list of logs
        """
        # Get all log records from the database
        logs = Log.objects.filter(user=request.auth.user)

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(gametype__id=game_type)

        serializer = LogSerializer(
            logs, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single log

        Returns:
            Response -- JSON serialized log instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            log = Log.objects.get(pk=pk)
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)    

# class UserSerializer(serializers.ModelSerializer):
#     """JSON serializer for event organizer's related Django user"""
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']

class LogSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializer type
    """
    class Meta:
        model = Log
        fields = ('id', 'user', 'type', 'journal', 'date', 'time')
        depth = 1
             

        