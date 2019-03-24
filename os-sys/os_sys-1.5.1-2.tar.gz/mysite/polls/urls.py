from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feedback/<str:vote>/', views.feedback, name='feedback')
]
