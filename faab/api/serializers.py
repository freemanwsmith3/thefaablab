from statistics import mean
from rest_framework import serializers
from .models import Player, Bid, Target


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'team')

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('value', 'target', 'user', 'week')

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('player', 'week')
