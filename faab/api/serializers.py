from statistics import mean
from rest_framework import serializers
from .models import Player, Bid


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'team', 'mean_value')

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('value', 'player', 'user')

