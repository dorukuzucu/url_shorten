from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from url_shorten_api.core.models import ShortenedUrl
from .serializers import RegisterSerializer, ShortenBodySerializer, ShortenUrlSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        content = {"email": user.email, "username": user.username}

        return Response(status=201, data=content)


@api_view(["get"])
@permission_classes([IsAuthenticated])
def get_user_urls(request):
    user = request.user
    urls = ShortenedUrl.objects.filter(user=user)
    if not len(urls):
        return Response(status=status.HTTP_204_NO_CONTENT, data={"Error": "No url found for given user"})
    serializer = ShortenUrlSerializer(urls, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(["post"])
@permission_classes([IsAuthenticated])
def shorten_url(request):
    user = request.user
    serializer = ShortenBodySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payload = serializer.data
    query_result = ShortenedUrl.objects.filter(shortened_url=payload["shortened_url"])
    if len(query_result):
        return Response(status=409,
                        data={"error": "Url "+payload["shortened_url"]+" already exists"})

    shortened_url = ShortenedUrl.objects.create(
        user=user,
        original_url=payload["original_url"],
        shortened_url=payload["shortened_url"]
    )

    content = {"original_url": shortened_url.original_url, "shortened_url": shortened_url.shortened_url}
    return Response(status=200, data=content)


@api_view(["delete"])
@permission_classes([IsAuthenticated])
def delete_url(request, url_id):
    user = request.user
    try:
        shortened_url = ShortenedUrl.objects.get(user=user, id=url_id)
        shortened_url.delete()
        return Response(status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': "url does not exist"}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["get"])
def redirect(request, url_path):
    print(url_path)
    try:
        shortened_url = ShortenedUrl.objects.get(shortened_url=url_path)
        return HttpResponseRedirect(shortened_url.original_url)
    except ObjectDoesNotExist:
        return Response(status=404, data={"error": "url {} is not found".format(url_path)})
