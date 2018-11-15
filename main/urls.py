from django.http import HttpResponse
from django.urls import path


def root_route(request):
    return HttpResponse('Test')

urlpatterns = [
    path('', root_route),
]
