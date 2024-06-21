from statistics import mean
from rest_framework import serializers
from .models import *

class PlayerRankingSerializer(serializers.ModelSerializer):
    abbreviation = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    position_type = serializers.SerializerMethodField()
    avg_rank = serializers.SerializerMethodField()
    ecr = serializers.SerializerMethodField()
    opp = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'team', 'team_name','abbreviation', 'position_type', 'link', 'image', 'avg_rank', 'ecr', 'opp')
    def get_abbreviation(self, obj):

        abbreviation = obj.team.abbreviation

        return abbreviation

    def get_team_name(self, obj):

        team_name = obj.team.team_name

        return team_name
    
    def get_position_type(self, obj):

        position_type = obj.position.position_type
        return position_type
        
    def get_avg_rank(self, obj):
        return obj.avg_rank
    
    def get_ecr(self, obj):
        ecr = None
        if hasattr(obj, 'ecr'):
            ecr = obj.ecr
        return ecr
    
    
    def get_opp(self, obj):
        opp = None
        if hasattr(obj, 'opp'):
            opp = obj.opp

        return opp


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['position_type']


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'team', 'position', 'link', 'image']

    def get_team(self, obj):
        return obj.team.team_name

    def get_position(self, obj):
        return obj.position.position_type



class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('value', 'player', 'user', 'week')

class TargetSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Target
        fields = ('player', 'week')

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ('rank', 'Player', 'week', 'user','created_at')

# class PlayerWithRankingSerializer(serializers.ModelSerializer):
#     rank = serializers.SerializerMethodField()

#     class Meta:
#         model = Player
#         fields = ['id', 'name', 'team', 'link', 'image', 'rank']

#     def get_rank(self, obj):
#         ranking = Ranking.objects.filter(Player=obj).first()
#         return ranking.rank if ranking else None