"""
URL configuration for schoolproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging
import time

from django.contrib import admin
from django.urls import path, include
from django.http.response import JsonResponse


LOGGER = logging.getLogger(__name__)


def sleep(request, timeout: int):
    LOGGER.info("处理: %d", timeout)
    time.sleep(timeout)
    LOGGER.info("处理完毕: %d", timeout)
    return JsonResponse({"timeout": timeout})


def proxy(request):
    response = JsonResponse({})
    response.headers = {
            "django": "proxy",
            "Access-Control-Allow-Origin": "cors.ramwin.com",
    }
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('proxy/', proxy),
    path('api/django-commands/', include("django_commands.urls")),
    path("sleep/<int:timeout>/", sleep),
]
