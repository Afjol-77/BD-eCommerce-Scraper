"""
URL configuration for scraper project.

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
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views
from django.conf.urls.static import static
from django.conf import settings
from evaly.views import evaly_dataset
from gadgetandgear.views import gadgetandgear_dataset
from bdshop.views import bdshop_dataset
from multiple.views import multiple_dataset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('evaly/', include('evaly.urls')),
    path('evaly_dataset', evaly_dataset, name="evaly_dataset"), ## Must not include \ after path, otherwise directory will change

    path('gng/', include('gadgetandgear.urls')),
    path('gng_dataset', gadgetandgear_dataset, name="gng_dataset"),

    path('bdshop/', include('bdshop.urls')),
    path('bdshop_dataset', bdshop_dataset, name="bdshop_dataset"),

    path('multiple/', include('multiple.urls')),
    path('multiple_dataset', multiple_dataset, name="multiple_dataset"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

