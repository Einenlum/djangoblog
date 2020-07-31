from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from ..forms import CustomUserCreationForm
from . import article, author, category


def handler404(request: HttpRequest, exception, template_name="error_404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response



class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
