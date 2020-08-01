from django.http import HttpRequest, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

from ..forms import CustomUserCreationForm
from . import article, author, category

def handler403(request: HttpRequest, exception, template_name="error_403.html"):
    response = render(request, template_name, {'exception': exception})
    response.status_code = 403
    return response

def handler404(request: HttpRequest, exception, template_name="error_404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        if settings.DISABLE_SIGNUP:
            raise PermissionDenied('Sorry, signup is disabled for now.')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.DISABLE_SIGNUP:
            raise PermissionDenied('Sorry, signup is disabled for now.')

        return super().post(request, *args, **kwargs)