from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('player', index),
    path('week/<int:weekNumber>', index),
    path('week/<int:weekNumber>/<str:playerName>', index),
    path('rankings/<int:weekNumber>', index),
    path('articles/vegas-versus-wr-adp', index)
    #path('create', index),
    #path('join/1', index)
]