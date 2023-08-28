from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When, Avg, Q, IntegerField, Min
from rest_framework import generics, status
from .serializers import *
from .models import Player, Bid, Target, Ranking
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from itertools import chain
from scipy import stats

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
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        week = request.GET.get(self.lookup_url_kwarg)
        if week != None:
            targets = Target.objects.filter(week=week)
            if 0 <= int(week) < 18:
                data = TargetSerializer(targets, many=True).data
                #data['is_user'] = self.request.session.session_key == bid.host


                return Response(data, status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Week'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Week Not Provided'}, status=status.HTTP_404_NOT_FOUND)
        
class BidView(APIView):
    serializer_class = BidSerializer

    def post(self, request, format=None):

        ###############
        ##  SESSION KEY HERE
        ##############
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data=request.data
        data['user'] = self.request.session.session_key 
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            value = serializer.data.get('value')
            target = serializer.data.get('target')
            week = serializer.data.get('week')
            user = self.request.session.session_key
            if 0 <= value <= 100 and 0 <= week <=17:

                ###############
                ## make a better way to avoid zero bids
                ############
                bid = Bid(user=user, value = value, week = week, target = Target.objects.get(id = target))
                bid.save()


                try:

                    this_week_vis_dict = self.request.session.get('visible_targets')
                    #print("OLD DICTK", this_week_vis_dict)
                    this_week_vis_list = this_week_vis_dict[str(week)]
                    this_week_vis_list.append(target)
                    this_week_vis_dict[str(week)] = this_week_vis_list
                    self.request.session['visible_targets'] = this_week_vis_dict
                    #print("NEW_DICT", self.request.session['visible_targets'][str(week)])
                except Exception as e:
                    print("No Session Key", e)

                # targets_dict = {}
                # weekly_bids = []

                # if str(week) not in self.request.session.get('visible_targets'):
                #     self.request.session.get('visible_targets')[str(week)] = weekly_bids
                #     print(weekly_bids)
                        
                # if target not in weekly_bids:
                #     weekly_bids.append(target)
                # targets_dict[str(week)] = weekly_bids
                # self.request.session['visible_targets']= targets_dict

                return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Bad Request':'Invalid Value or Week'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Bad Request':'Invalid Bid'}, status=status.HTTP_400_BAD_REQUEST)

class TargetsAPI(APIView):

    week = 'week'

    def get(self,request,format=None):
        week = request.GET.get(self.week)


        ###################
        current_week = 16
        ########################

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
            
        vis_targs_bool = []
        
        targets = Target.objects.filter(week=week)
        targets = sorted(targets, key=lambda t: t.num_valid_bids, reverse=True)
        if not self.request.session.get('visible_targets') or str(week) not in self.request.session.get('visible_targets'):
            target_dict = {}
            target_dict[str(week)] = []
            self.request.session['visible_targets'] = target_dict
            

        names = []
        teams = []
        links = []
        images = []
        positions = []
        mean_values = []
        mode_values = []
        median_values = []
        num_bids = []
        target_ids = []
        vis_targs_bool = []
        
        for d in targets:

            if d.id in self.request.session.get('visible_targets')[str(week)] or current_week > int(week):
                vis_targs_bool.append(True)

            else:
                vis_targs_bool.append(False)

            names.append(d.player.name)
            teams.append(d.player.team.team_name)
            links.append(d.player.link)
            images.append(d.player.image)
            positions.append(d.player.position.position_type)
            target_ids.append(d.id)
            num_bids.append(d.num_valid_bids)
            try:
                mean_values.append(round(d.mean_value, 2))
            except:
                mean_values.append(0)
            
            try:
                median_values.append(round(d.median_value, 2))
            except:
                median_values.append(0)
            try:
                mode_values.append(round(d.mode_value, 2))
            except:
                mode_values.append(0)                



            #bids = Bid.objects.filter(target = d.id, value__range = [1, 100]).values_list('value', flat=True)



        data = {
            'visibleTargets': vis_targs_bool,
            'names': names,
            'teams': teams,
            'links' : links,
            'images': images,
            'targets': target_ids,
            'positions': positions,
            'mean_values' : mean_values,
            'mode_values' : mode_values,
            'median_values' : median_values,
            'num_bids': num_bids,
        }
        
        
        return JsonResponse(data, status=status.HTTP_200_OK)

class DataAPI(APIView):
    week_target = 'week'
    def get(self,request,format=None):
        

        week_name = request.GET.get(self.week_target).split('?target=')

        week = week_name[0]
        target_id = week_name[1]
        flat_vals = list(Bid.objects.filter(week=week, target_id=target_id, value__range = [1, 100]).order_by('value').values_list('value', flat=True))


        if flat_vals:
            low_range = flat_vals[int(len(flat_vals)*.1)]
            high_range = flat_vals[int(len(flat_vals)*.9)]


        ###############################ge
        ######## Be careful of weird random bins 
        ##############################

        first_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [low_range,  round((1)*(high_range- low_range)/6 +  low_range)]).count()
        second_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((1)*(high_range- low_range)/6 +  low_range), round((2)*(high_range- low_range)/6 +  low_range)]).count()
        third_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((2)*(high_range- low_range)/6 +  low_range), round((3)*(high_range- low_range)/6 +  low_range)]).count()
        fourth_bin = Bid.objects.filter(week=week, target_id=target_id, value__range =[ round((3)*(high_range- low_range)/6 +  low_range), round((4)*(high_range- low_range)/6 +  low_range)]).count()
        fifth_bin = Bid.objects.filter(week=week, target_id=target_id, value__range =[ round((4)*(high_range- low_range)/6 +  low_range), round((5)*(high_range- low_range)/6 +  low_range)]).count()
        sixth_bin= Bid.objects.filter(week=week, target_id=target_id, value__range = [ round((5)*(high_range- low_range)/6 +  low_range), high_range]).count()

        data = {
            "first_bin": first_bin,
            "second_bin": second_bin,
            "third_bin": third_bin,
            "fourth_bin": fourth_bin,
            "fifth_bin": fifth_bin,
            "sixth_bin": sixth_bin,

            "first_name": str(low_range) + '-' + str(round((1)*(high_range- low_range)/6 +low_range)),
            "second_name": str(round((1)*(high_range- low_range)/6 +low_range)) + '-' + str(round((2)*(high_range- low_range)/6 +low_range)),
            "third_name": str(round((2)*(high_range- low_range)/6 +low_range)) + '-' + str(round((3)*(high_range- low_range)/6 +low_range)),
            "fourth_name": str(round((3)*(high_range- low_range)/6 +low_range)) + '-' + str(round((4)*(high_range- low_range)/6 +low_range)),
            "fifth_name": str(round((4)*(high_range- low_range)/6 +low_range)) + '-' + str(round((5)*(high_range- low_range)/6 +low_range)),
            "sixth_name": str(round((5)*(high_range- low_range)/6 +low_range)) + '-' + str(high_range),

        }
        return JsonResponse(data)

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
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        print(self.request.session.session_key)
        data=request.data
        user = self.request.session.session_key 
        player = Player.objects.get(id=data['playerid'])
        
        #print(serializer.data)
        try:  
    
            ranking = Ranking(user=user,rank=data['rank'], Player=player, week = data['week'])
            ranking.save()
            return Response(RankingSerializer(ranking).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)     
            return Response({'Bad Request':'Invalid Rank'}, status=status.HTTP_400_BAD_REQUEST)