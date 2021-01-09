from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.each_country,name='django-stats'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

