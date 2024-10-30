"""
URL configuration for ELEC9609 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from ELEC9609 import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('admin/', admin.site.urls),
    path('api/', views.api),
    path('hello_world/', views.hello_world),
    path('hello_world/<int:test_id>', views.hello_world_test),
    path('api/cookies_get_csrf_token', views.api_cookies_get_csrf_token),
    path('api/get_csrf_token', views.api_get_csrf_token),
    path('api/upload_file', views.api_upload_file),
    path('media/<path:file_path>', views.get_media_file),
    path('rest/user', views.rest_user),
    path('rest/user_avatar', views.rest_user_avatar),
    path('rest/pet', views.rest_pet),
    path('rest/pet_avatar', views.rest_pet_avatar),
    path('rest/provider', views.rest_provider),
    path('rest/trainer', views.rest_trainer),
    path('rest/trainer_avatar', views.rest_trainer_avatar),
    path('rest/service_order', views.rest_service_order),
    path('rest/payment', views.rest_payment),
    path('rest/pethelp', views.rest_pethelp_ai),
    path('.well-known/pki-validation/<str:filename>', views.verify_ssl)
]
