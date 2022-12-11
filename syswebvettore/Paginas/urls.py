from django.urls import path
from .views import IndexView, SobreView


urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('register/', SobreView.as_view(), name='register'),
    path('tables/', SobreView.as_view(), name='tables'),
]
