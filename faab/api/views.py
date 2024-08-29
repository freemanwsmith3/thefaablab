from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When, Avg, Q, IntegerField, Min, OuterRef, Subquery
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from itertools import chain
from scipy import stats
from django.contrib.sessions.backends.db import SessionStore  # 
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
import numpy as np
from statistics import mean, median, mode

def sort_queryset_by_ids(queryset, ids):
    # Prepare the ordering using the Case/When expressions
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)], output_field=IntegerField())

    # Annotate the queryset with the ordering and then sort by it
    return queryset.annotate(sort_order=preserved_order).order_by('sort_order')

class PlayerView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class GetWeek(APIView):
    serializer_class = TargetSerializer
    lookup_url_kwarg = 'week'


    def get(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        week = request.GET.get(self.lookup_url_kwarg)
        if week != None:
            print('targets')
            targets = Target.objects.filter(week=week)
            if 0 <= int(week) :
                data = TargetSerializer(targets, many=True).data
                #data['is_user'] = request.session.session_key == bid.host


                return Response(data, status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Week'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Week Not Provided'}, status=status.HTTP_404_NOT_FOUND)
        
class BidView(APIView):
    serializer_class = BidSerializer

    def post(self, request, format=None):
        # print(request.session.session_key)
        # print(';;;;;;;;;;;')
        ###############
        ##  SESSION KEY HERE
        ##############
        # if not request.session.exists(request.session.session_key):
        #     print('creating session')
        #     request.session.create()

        data=request.data
        data['user'] = 'none'
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            value = serializer.data.get('value')
            player = serializer.data.get('player')
            week = serializer.data.get('week')
            user = 'none'
            if 0 <= value <= 200 :

                ###############
                ## make a better way to avoid zero bids
                ############
                if value > 0:
                    bid = Bid(user=user, value = value, week = week, player = Player.objects.get(id = player))
                    bid.save()

                    return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
                else: 
                    return Response({'Zero Bid: Display Results'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Bad Request':'Invalid Value or Week'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('invalid serializer')
            return Response({'Bad Request':'Invalid Bid'}, status=status.HTTP_400_BAD_REQUEST)
        
class TargetsAPI(APIView):
    def get(self, request, format=None):
        week = request.query_params.get('week')

        if week != '1000':
            targets = Target.objects.filter(week=week)
            players = Player.objects.filter(targets__in=targets).distinct()
        else:
            targets = Target.objects.filter(week=week).order_by('id')
            players = Player.objects.filter(targets__in=targets).distinct().order_by('targets__id')
        
        serializer = PlayerSerializer(players, many=True)
        
        return Response({
            'players': serializer.data
        }, status=status.HTTP_200_OK)
### this is the old version with sessions and before i split it into two: 
# class TargetsAPI(APIView):


#     def get(self, request, format=None):

#         week = request.query_params.get('week')
#         print(week)

#         # if not request.session.exists(request.session.session_key):
#         #     request.session.create()
#         #     print('Creating session')
#         # else:
#         #     print('Session exists:', request.session.session_key)


#         targets = Target.objects.filter(week=week)


#         # Step 2: Initialize the dictionary to store bids by target ID
#         binned_data_dict = defaultdict(list)
#         stats_dict = {}
#         # Step 3: For each target, retrieve the associated bids by matching the week and player
#         for target in targets:
#             player_id = target.player.id
#             target_bids = Bid.objects.filter(week=week, player=target.player)
#             bid_values = list(target_bids.values_list('value', flat=True))

#             # Step 4: Bin the bid values into 5 bins and format the data
#             if bid_values:
#                 average_bid = round(mean(bid_values), 1)
#                 median_bid = round(median(bid_values), 1)
#                 try:
#                     most_common_bid = mode(bid_values)
#                 except:
#                     most_common_bid = None  # Handle the case where there is no single mode
#                 number_of_bids = len(bid_values)
#                 bins = np.linspace(min(bid_values), max(bid_values), 5)  # Create 5 equal bins
#                 binned_data, _ = np.histogram(bid_values, bins=bins)
#                 bins = np.round(bins).astype(int)  # Round bins to integers
#                 for i in range(len(binned_data)):
#                     bin_key = f'{bins[i]} - {bins[i+1]}'
#                     binned_data_dict[str(player_id)].append({
#                         'label': bin_key,
#                         'bids': int(binned_data[i])
#                     })
#             else:
#                 # Default values when there are no bids
#                 average_bid = 'NA'
#                 median_bid = 'NA'
#                 most_common_bid = 'NA'
#                 number_of_bids = """You're the 1st bid"""
#                 binned_data = {}
#             stats_dict[str(player_id)] = {
#                 'averageBid': average_bid,
#                 'medianBid': median_bid,
#                 'mostCommonBid': most_common_bid,
#                 'numberOfBids': number_of_bids
#             }
#         # targets = sorted(targets, key=lambda t: t.num_valid_bids, reverse=True)
#         # Handle session visible_targets
#         # if not request.session.get('visible_targets'):
#         #     print('visible_targets key not found in session')
#         #     request.session['visible_targets'] = {}

#         # if str(week) not in request.session['visible_targets']:
#         #     print(f'Week {week} not in visible_targets')
#         #     request.session['visible_targets'][str(week)] = []

#         # print('visible_targets:', request.session['visible_targets'])

#         # # Save session explicitly
#         # request.session.modified = True
#         # request.session.save()
#         # print('Session data saved:', request.session.items())
#         # print('Session:', request.session)

#         targets = Target.objects.filter(week=week)

#         # Serialize the Player data with related Targets and Bids
#         players = Player.objects.filter(targets__in=targets).distinct()
#         serializer = PlayerSerializer(players, many=True)
#         # print(request.session.items())
#         # print(request.session.session_key)
#         return Response({
#             'players': serializer.data,
#             'binned_data': dict(binned_data_dict),
#             'stats': stats_dict
#         }, status=status.HTTP_200_OK)

class StatsAPI(APIView):

    def get(self, request, format=None):
        week = request.query_params.get('week')
        targets = Target.objects.filter(week=week)

        binned_data_dict = defaultdict(list)
        stats_dict = {}

        for target in targets:
            player_id = target.player.id
            target_bids = Bid.objects.filter(week=week, player=target.player)
            bid_values = list(target_bids.values_list('value', flat=True))

            if bid_values:
                average_bid = round(mean(bid_values), 1)
                median_bid = round(median(bid_values), 1)
                try:
                    most_common_bid = mode(bid_values)
                except:
                    most_common_bid = None
                number_of_bids = len(bid_values)
                bins = np.linspace(min(bid_values), max(bid_values), 5)
                binned_data, _ = np.histogram(bid_values, bins=bins)
                bins = np.round(bins).astype(int)
                for i in range(len(binned_data)):
                    bin_key = f'{bins[i]} - {bins[i+1]}'
                    binned_data_dict[str(player_id)].append({
                        'label': bin_key,
                        'bids': int(binned_data[i])
                    })
            else:
                average_bid = 'NA'
                median_bid = 'NA'
                most_common_bid = 'NA'
                number_of_bids = """You're the 1st bid"""
                binned_data = {}
            stats_dict[str(player_id)] = {
                'averageBid': average_bid,
                'medianBid': median_bid,
                'mostCommonBid': most_common_bid,
                'numberOfBids': number_of_bids
            }

        return Response({
            'binned_data': dict(binned_data_dict),
            'stats': stats_dict
        }, status=status.HTTP_200_OK)

# class DataAPI(APIView):
#     #week_target = 'week'
#     def get(self,request,format=None):
#         week = request.query_params.get('week')
#         # target_id = request.query_params.get('target')
    


#         # week = week_name[0]
#         # target_id = week_name[1]
#         flat_vals = list(Bid.objects.filter(week=week, target_id=target_id, value__range = [1, 100]).order_by('value').values_list('value', flat=True))


#         if flat_vals:
#             low_range = flat_vals[int(len(flat_vals)*.1)]
#             high_range = flat_vals[int(len(flat_vals)*.9)]


#         ###############################
#         ######## Be careful of weird random bins 
#         ##############################
#         bins_array = []
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range = [low_range,  round((1)*(high_range- low_range)/6 +  low_range)]).count())
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((1)*(high_range- low_range)/6 +  low_range), round((2)*(high_range- low_range)/6 +  low_range)]).count())
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((2)*(high_range- low_range)/6 +  low_range), round((3)*(high_range- low_range)/6 +  low_range)]).count())
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range =[ round((3)*(high_range- low_range)/6 +  low_range), round((4)*(high_range- low_range)/6 +  low_range)]).count())
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range =[ round((4)*(high_range- low_range)/6 +  low_range), round((5)*(high_range- low_range)/6 +  low_range)]).count())
#         bins_array.append(Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((5)*(high_range- low_range)/6 +  low_range), high_range]).count())
        
#         bin_dict_array = []
#         for bin_data in bins_array:
#             bin_dict = {}
#             bin_dict['bin'] = bin_data
#             bin_dict_array.append(bin_dict)
        

#         print(bin_dict_array)
#         data = {
#             'bins': bin_dict_array,
#             "first_name": str(low_range) + '-' + str(round((1)*(high_range- low_range)/6 +low_range)),
#             "second_name": str(round((1)*(high_range- low_range)/6 +low_range)) + '-' + str(round((2)*(high_range- low_range)/6 +low_range)),
#             "third_name": str(round((2)*(high_range- low_range)/6 +low_range)) + '-' + str(round((3)*(high_range- low_range)/6 +low_range)),
#             "fourth_name": str(round((3)*(high_range- low_range)/6 +low_range)) + '-' + str(round((4)*(high_range- low_range)/6 +low_range)),
#             "fifth_name": str(round((4)*(high_range- low_range)/6 +low_range)) + '-' + str(round((5)*(high_range- low_range)/6 +low_range)),
#             "sixth_name": str(round((5)*(high_range- low_range)/6 +low_range)) + '-' + str(high_range),

#         }
#         return JsonResponse(data)

class RankingAPI(APIView):
    week_target = 'week'
    def get(self,request, format=None):
        week_name = request.GET.get(self.week_target).split('?target=')

        week = week_name[0]

        players_with_avg_rank_and_ecr = (Player.objects
            .annotate(
                avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)),
                ecr=Min('rankings__rank', filter=Q(rankings__week=week, rankings__user='fantasy_pros'))
            )
            .order_by('avg_rank')
        )[0:250]
        serializer = PlayerRankingSerializer(players_with_avg_rank_and_ecr, many=True)
        return Response(serializer.data)

class VotingAPI(APIView):
    week_target = 'week'
    def get(self,request, format=None):
        week_name = request.GET.get(self.week_target).split('?target=')

        week = week_name[0]
        top_tier = random.randint(1, 49)
        mid_tier = random.randint(50, 99)
        low_tier = random.randint(100,150)
        top_tier_players = (Player.objects
                                .annotate(avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)))
                                .order_by('avg_rank'))[top_tier:top_tier+3]
        mid_tier_players = (Player.objects
                                .annotate(avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)))
                                .order_by('avg_rank'))[mid_tier:mid_tier+3]
        low_tier_players = (Player.objects
                                .annotate(avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)))
                                .order_by('avg_rank'))[low_tier:low_tier+3]    
                            
        voting_players = chain( top_tier_players, mid_tier_players, low_tier_players)
        
        serializer = PlayerRankingSerializer(voting_players, many=True)
        # for player in categories_with_avg_rank:
        #     print(player)
        #@sorted_players = sort_queryset_by_ids(players, player_ids)
        #print(type(sorted_players))

        return Response(serializer.data)

class VoteView(APIView):
    serializer_class = RankingSerializer
    def post(self, request, format=None):

        ###############
        ##  SESSION KEY HERE
        ##############
        if not request.session.exists(request.session.session_key):
            request.session.create()
        print(request.session.session_key)
        data=request.data
        user = request.session.session_key 
        player = Player.objects.get(id=data['playerid'])
        
        #print(serializer.data)
        try:  
    
            ranking = Ranking(user=user,rank=data['rank'], Player=player, week = data['week'])
            ranking.save()
            return Response(RankingSerializer(ranking).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)     
            return Response({'Bad Request':'Invalid Rank'}, status=status.HTTP_400_BAD_REQUEST)

class WeeklyRankingAPI(APIView):
    week_target = 'week'

    def get(self,request, format=None):
        week_name = request.GET.get(self.week_target).split('?week=')

        week = week_name[0]
        print(week)
        qbs = (Player.objects
                .filter(position_id=3)
                .annotate(
                    avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week, position_id = 3)),
                    ecr=Min('rankings__rank', filter=Q(rankings__week=week, rankings__user='fantasy_pros'))
                )
                .order_by('avg_rank')
        )[0:25]
        wrs = (Player.objects
                .filter(position_id=2)
                .annotate(
                    avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week, position_id = 2)),
                    ecr=Min('rankings__rank', filter=Q(rankings__week=week, rankings__user='fantasy_pros'))
                )
                .order_by('avg_rank')
        )[0:50]
        rbs = (Player.objects
                .filter(position_id=1)
                .annotate(
                    avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week, position_id = 1)),
                    ecr=Min('rankings__rank', filter=Q(rankings__week=week, rankings__user='fantasy_pros'))
                )
                .order_by('avg_rank')
        )[0:50]
        tes = (Player.objects
                .filter(position_id=4)
                .annotate(
                    avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week, position_id = 4)),
                    ecr=Min('rankings__rank', filter=Q(rankings__week=week, rankings__user='fantasy_pros'))
                )
                .order_by('avg_rank')
        )[0:25]
        players_with_avg_rank_and_ecr = chain( qbs, wrs, rbs, tes)
        serializer = PlayerRankingSerializer(players_with_avg_rank_and_ecr, many=True)
        return Response(serializer.data)

class WeeklyVotingAPI(APIView):
    week_target = 'week'
    def get(self,request, format=None):
        week_name = request.GET.get(self.week_target).split('?week=')

        week = week_name[0]

        opponent_subquery = Ranking.objects.filter(
            Player_id=OuterRef('id'),
            week=week,
            user='fantasy_pros'
        ).values('opponent__abbreviation')[:1]



        qb_ran = random.randint(1, 23)
        rb_tier = random.randint(1, 48)
        wr_tier = random.randint(1, 48)
        te_tier = random.randint(1, 23)
        qbs = (Player.objects.filter(position_id=3)
                                .annotate(avg_rank=Avg('rankings__rank',  filter=Q(rankings__week=week)), opp=Subquery(opponent_subquery))
                                .order_by('avg_rank'))[qb_ran:qb_ran+3]
        wrs = (Player.objects.filter(position_id=2)
                                .annotate(avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)), opp=Subquery(opponent_subquery))
                                .order_by('avg_rank'))[wr_tier:wr_tier+3]
        rbs = (Player.objects.filter(position_id=1)
                                .annotate(avg_rank=Avg('rankings__rank',  filter=Q(rankings__week=week)), opp=Subquery(opponent_subquery))
                                .order_by('avg_rank'))[rb_tier:rb_tier+3]    
        tes = (Player.objects.filter(position_id=4)
                                .annotate(avg_rank=Avg('rankings__rank', filter=Q(rankings__week=week)), opp=Subquery(opponent_subquery))
                                .order_by('avg_rank'))[te_tier:te_tier+3]    
                            
        voting_players = chain( qbs, wrs, rbs, tes)
        print(voting_players)
        serializer = PlayerRankingSerializer(voting_players, many=True)
        # for player in categories_with_avg_rank:
        #     print(player)
        #@sorted_players = sort_queryset_by_ids(players, player_ids)
        #print(type(sorted_players))

        return Response(serializer.data)

# class WeeklyVoteView(APIView):
#     serializer_class = RankingSerializer
#     def post(self, request, format=None):

#         ###############
#         ##  SESSION KEY HERE
#         ##############
#         if not request.session.exists(request.session.session_key):
#             request.session.create()
#         print(request.session.session_key)
#         data=request.data
#         user = request.session.session_key 
#         player = Player.objects.get(id=data['playerid'])
        
#         #print(serializer.data)
#         try:  
    
#             ranking = Ranking(user=user,rank=data['rank'], Player=player, week = data['week'])
#             ranking.save()
#             return Response(RankingSerializer(ranking).data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             print(e)     
#             return Response({'Bad Request':'Invalid Rank'}, status=status.HTTP_400_BAD_REQUEST)