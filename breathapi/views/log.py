"""View module for handling requests about logs"""
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
    """Let's Breathe logs"""


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
            Response -- JSON serialized log instance
        """
        log = Log.objects.get(pk=pk)
        log.user = request.auth.user
        log.date = log.date
        log.journal = request.data["journal"]
        time = Time.objects.get(pk=request.data["time"])
        log.time = time
        type = Type.objects.get(pk=request.data["type"])
        log.type = type
        
        log.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

       

    def create(self, request):
        """Handle POST operations for logs

        Returns:
            Response -- JSON serialized log instance
        """
        log = Log()
        log.user = request.auth.user
        log.date = request.data["date"]
        log.journal = request.data["journal"]
        time = Time.objects.get(pk=request.data["time"])
        log.time = time
        type = Type.objects.get(pk=request.data["type"])
        log.type = type
       

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
            #   http://localhost:8000/logs/2
            #
            # The `2` at the end of the route becomes `pk`
            log = Log.objects.get(pk=pk)
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)    



class LogSerializer(serializers.ModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializer type
    """
    class Meta:
        model = Log
        fields = ('id', 'user', 'type', 'journal', 'date', 'time')
        depth = 1
             

        