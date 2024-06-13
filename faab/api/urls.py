"""faab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from .views import PlayerView, BidView,GetWeek, TargetsAPI, RankingAPI, VotingAPI, VoteView, WeeklyRankingAPI, WeeklyVotingAPI


urlpatterns = [
    path('player', PlayerView.as_view()),
    path('bid', BidView.as_view()), 
    path('vote', VoteView.as_view()), 
    # path('weekly-vote', WeeklyVoteView.as_view()), 
    path('get-week', GetWeek.as_view() ),
    path('get-targets', TargetsAPI.as_view()),
    # path('get-data', DataAPI.as_view()),
    path('get-weekly-rankings', WeeklyRankingAPI.as_view()),
    path('get-rankings', RankingAPI.as_view()),
    path('get-weekly-voting', WeeklyVotingAPI.as_view()),
    path('get-voting', VotingAPI.as_view()),
]

