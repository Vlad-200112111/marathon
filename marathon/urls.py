from django.urls import include, path
from .views import *


urlpatterns = [
    path("generate-fake-data/", GenerateFakeDataApiView.as_view()),
]