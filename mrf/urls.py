from django.urls import path

from mrf import views

urlpatterns = [
    path('/', views.index, name='index'),
]
