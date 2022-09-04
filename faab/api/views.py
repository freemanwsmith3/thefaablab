from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import PlayerSerializer,BidSerializer
from .models import Player, Bid
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
# class PlayerView(generics.CreateAPIView):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer

class PlayerView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class BidView(APIView):
    serializer_class = BidSerializer



    def post(self, request, format=None):

        ###############
        ##  SESSION KEY HERE
        ##############
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            value = serializer.data.get('value')
            player = serializer.data.get('player')
            user = self.request.session.session_key
            
            #################
            ##
            ##
            # DELETE THIS FOR SESSION KEY

            ######

            user = serializer.data.get('user')
            
            
            
            queryset = Bid.objects.filter(user=user)
            if queryset.exists():
                print("here show the value", queryset)
            else:
                bid = Bid(user=user, value = value, player = Player.objects.get(id = player))
                bid.save()
            
            return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)