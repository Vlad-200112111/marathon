"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from django.conf.urls.static import static
from django.conf import settings

from marathon.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('marathon.urls')),
    path('', IndexView.as_view(), name='index'),
    path('register-as-runner/', RegisterAsRunnerView.as_view(), name='register_as_runner'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('sponsor/', SponsorView.as_view(), name='sponsor'),
    path('about/', AboutView.as_view(), name='about'),
    path('bmi/', BMIView.as_view(), name='bmi'),
    path('bmr/', BMRView.as_view(), name='bmr'),
    path('charitable-organizations/', CharitableOrganizationView.as_view(), name='charitable_organizations'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
