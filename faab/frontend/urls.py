from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('player', index),
    path('week/<int:weekNumber>', index)
    #path('join', index),
    #path('create', index),
    #path('join/1', index)
]