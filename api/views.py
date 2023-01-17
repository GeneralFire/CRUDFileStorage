from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from storage.serializers import FileSerializer
from storage.models import File


@api_view(['GET'])
def get_routes(request: HttpRequest):
    routes = [

        {'GET': '/'},               # help
        {'POST': '/api/login'},     # get token
        {'DELETE': '/api/login'},   # delete token

        # get files
        {'GET': '/api/storage/'},
        # upload file
        {'POST': '/api/storage/'},
        # download file
        {'GET': '/api/storage/id'},
        # delete file
        {'DELETE': '/api/storage/id'},
        # change file properties
        {'UPDATE': '/api/storage/id'},

    ]

    return Response(routes)


@api_view(['GET'])
def get_files(request: HttpRequest):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_file(request: HttpRequest, pk):
    file = File.objects.get(id=pk)
    if not file:
        return Response(status=status.HTTP_404_NOT_FOUND)
    file.delete()
    return Response(status=status.HTTP_200_OK)
