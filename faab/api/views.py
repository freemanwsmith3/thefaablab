from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from .serializers import PlayerSerializer,BidSerializer, TargetSerializer
from .models import Player, Bid, Target
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy
from scipy import stats


# Create your views here.
# class PlayerView(generics.CreateAPIView):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer

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
            if 0 < int(week) < 18:
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
            
            if 0 <= value <= 100 and 1 <= week <=17:

                bid = Bid(user=user, value = value, week = week, target = Target.objects.get(id = target))
                bid.save()
                targets_dict = {}
                weekly_bids = []

                if self.request.session.get('visible_targets'):
                    
                    targets_dict = self.request.session.get('visible_targets')
                
                    if targets_dict[str(week)]:

                        weekly_bids = targets_dict[str(week)]

                        
                if target not in weekly_bids:
                    weekly_bids.append(target)
                targets_dict[str(week)] = weekly_bids
                self.request.session['visible_targets']= targets_dict

                return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Bad Request':'Invalid Value or Week'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({'Bad Request':'Invalid Bid'}, status=status.HTTP_400_BAD_REQUEST)

class TargetsAPI(APIView):

    lookup_url_kwarg = 'week'

    def get(self,request,format=None):
        week = request.GET.get(self.lookup_url_kwarg)

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        vis_targs_bool = []
        if not self.request.session.get('visible_targets'):
            targets_dict = {}
            targets_dict[str(week)] = vis_targs_bool
            self.request.session['visible_targets']= targets_dict
        
        targets = Target.objects.filter(week=week)
        for targ in range(len(targets)):
            if targ in self.request.session.get('visible_targets')[str(week)]:
                vis_targs_bool.append(True)
            else:
                vis_targs_bool.append(False)

        names = []
        teams = []
        positions = []
        mean_values = []
        mode_values = []
        median_values = []
        num_bids = []
        for d in targets:
            #names.append(Player.objects.get(id = d['player']).name)
            #teams.append(Player.objects.get(id = d['player']).team)
            #positions.append(Player.objects.get(id = d['player']).position)
            names.append(d.player.name)
            teams.append(d.player.team)
            positions.append(d.player.position)
            bids = Bid.objects.filter(target = d.id).values_list('value', flat=True)
            num_bids.append(len(bids))
            mean_values.append(round(numpy.mean(bids), 2))
            mode_values.append(int(stats.mode(bids, keepdims=False)[0]))
            median_values.append(round(numpy.median(bids), 2))

        # data['names'] += names
        # data['teams'] += teams
        # data['positions'] += positions


        data = {
            'visibleTargets': vis_targs_bool,
            'names': names,
            'teams': teams,
            'positions': positions,
            'mean_values' : mean_values,
            'mode_values' : mode_values,
            'median_values' : median_values,
            'num_bids': num_bids,
        }
        print(data)

        return JsonResponse(data, status=status.HTTP_200_OK)