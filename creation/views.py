from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.list import ListView
from dayplanner.services import yelp_client
from django.contrib.auth.models import User
from resources.days.models import Day, DayVenue
from resources.venues.models import Venue

class DayvenueListView(ListView):
    model = DayVenue
    template_name = "creation/_dayvenue_list.html"
    context_object_name = "dayvenue_list"

    def get_context_data(self, **kwargs):
        context = super(DayvenueListView, self).get_context_data(**kwargs)
        context["dayVenue"] = get_object_or_404(Day, id=self.kwargs["pk"])
        return context

    def get_queryset(self):
        queryset = super(DayvenueListView, self).get_queryset()
        return queryset.filter(day__id=self.kwargs["pk"])

def searchPage(request, day_id):
    # Initializing the context dict
    context = {}
    # Given day_id try to access the day object
    day = get_object_or_404(Day, pk=day_id)
    context["day"] = day
    
    if request.method == "GET":
        # Case the the user send a GET URL with a query String Yelp_id:<id>
        # For example: /creation/editday/1?yelp_id=x86
        # Is User want to added x86 into day 1
        if request.GET.get("yelp_id"):
            # The function addVenue Defined at line 32
            # Add Venue into current selected day and refresh the page
            return addVenue(request, day)
        return render(request, "creation/_search.html", context)

    elif request.method == "POST":
        if request.GET.get("search"):
            return search(request, context)


def addVenue(request, day):
    yelp_id = request.GET.get("yelp_id")
    venue, created = Venue.objects.get_or_create(yelp_id=yelp_id)
    DayVenue.objects.create(day=day, venue=venue, pos=day.dayvenue_set.count() + 1)
    rootpath = request.path.split("?")[0]

    return HttpResponseRedirect(rootpath)


def search(request, context):
    # handle Search action in creation/editday?<day_id>
    user_input_param1 = request.POST["user_input_term"]
    user_input_param2 = request.POST["user_input_location"]

    bussiness_data = yelp_client.search(user_input_param1, user_input_param2)
    context["search_results"] = bussiness_data["businesses"]

    return render(request, "creation/_search.html", context)


def deleteday(request):
    day_id = request.GET.get("day_id")
    if not day_id:
        return HttpResponse("--- Deletion request cannot be processed")
    try:
        day = Day.objects.get(id=day_id, is_active=True)
        day.is_active = False
        day.save()
    except Exception as e:
        print("-- deletion error %s") % (e)

    return HttpResponseRedirect("/creation")


def daylist(request):
    # userName is in string
    # Example: login as Admin the userName == "admin"
    if request.method == "POST":
        # create a new day here
        dayname = request.POST["day_name"]
        Day.objects.create(creator=request.user, name=dayname)

    userObject = request.user
    context = {
        "userDayList": userObject.day_set.all().filter(is_active=True),
        "username": userObject.username,
    }
    return render(request, "creation/_day_list.html", context)   