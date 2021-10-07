from django.shortcuts import render
from django.http import JsonResponse

from venues.models import Venue

# Create your views here.

def detail(request, venue_id):
    v = Venue.objects.get(pk=venue_id)
    return JsonResponse({'yelp_id': v.yelp_id})