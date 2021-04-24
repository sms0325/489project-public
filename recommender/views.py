from django.shortcuts import render
from .forms import EnterProfInfo

def index(request):
    if request.method == "POST":
        if "search-prof" in request.POST:
            form = EnterProfInfo(request.POST)
            prof_name = request.POST.get("state")
            topic = request.POST.get("county")
    else:
        form = EnterProfInfo()
    return render(request, 'index.html')


#from 315 project - using as reference for my own view.
#     #calendars, calendar_names = list_calendars()
#     events = ""
#                 #calendarId = calendars[calendar]['id'] #accessing a calendar's ID by its name
#     elif request == "GET":
#         if "view_calendar" in request.GET:
#             btn_submit = request.GET.get("btn-submit")
#             events = export_from_firebase(email)

# Create your views here.
