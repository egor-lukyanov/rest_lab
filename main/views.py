from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework import viewsets, views
from rest_framework.response import Response

from main.models import Job, JobResult
from main.serializers import JobResultSerializer, JobSerializer
from rest_lab.utils import simple, big_data, fib


class JobViewSet(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobResultViewSet(viewsets.ModelViewSet):

    queryset = JobResult.objects.all()
    serializer_class = JobResultSerializer


class SimpleView(views.APIView):

    def get(self, request):
        return JsonResponse(simple())


class BigView(views.APIView):

    def get(self, request):
        return StreamingHttpResponse(streaming_content=big_data(), content_type='application/json')


class CPUView(views.APIView):

    def get(self, request):
        return HttpResponse(fib())


class PingView(views.APIView):

    def get(self, request):
        return HttpResponse('ok')