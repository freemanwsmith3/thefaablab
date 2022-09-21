from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
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
        current_week = 3
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
            mean_values.append(round(d.mean_value, 2))
            median_values.append(d.median_value)
            mode_values.append(d.mode_value)
            bids = Bid.objects.filter(target = d.id, value__range = [1, 100]).values_list('value', flat=True)



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

        
        interval = int((high_range - low_range) / 6)

        ###############################
        ######## Be careful of weird random bins 
        ##############################

        first_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [low_range, interval+low_range]).count()
        second_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [interval+low_range+1, 2*interval+low_range]).count()
        third_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [2*interval+low_range+1, 3*interval+low_range]).count()
        fourth_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [3*interval+low_range+1, 4*interval+low_range+1]).count()
        fifth_bin = Bid.objects.filter(week=week, target_id=target_id, value__range = [4*interval+low_range+2, 5*interval+low_range+1]).count()
        sixth_bin= Bid.objects.filter(week=week, target_id=target_id, value__range = [5*interval+low_range+2, high_range]).count()

        data = {
            "first_bin": first_bin,
            "second_bin": second_bin,
            "third_bin": third_bin,
            "fourth_bin": fourth_bin,
            "fifth_bin": fifth_bin,
            "sixth_bin": sixth_bin,

            "first_name": str(low_range) + '-' + str(interval+low_range),
            "second_name": str(interval+low_range+1) + '-' + str(2*interval+low_range),
            "third_name": str(2*interval+low_range+1) + '-' + str(3*interval+low_range),
            "fourth_name": str(3*interval+low_range+1) + '-' + str(4*interval+low_range+1),
            "fifth_name": str(4*interval+low_range+2) + '-' + str(5*interval+low_range+1),
            "sixth_name": str(5*interval+low_range+2) + '-' + str(high_range),

        }
        return JsonResponse(data)

