from django.shortcuts import render
from .forms import EnterProfInfo
from .rec import get_topics_for_coauthor, get_coauthors_as_edge_list
#import functions from other files here

def index(request):
    form = ""
    if request.method == "POST":
        if "search-prof" in request.POST:
            form = EnterProfInfo(request.POST)
            author_id = request.POST.get("state")
            topic = request.POST.get("county")
            coauthor_topics = get_id(author_id)
    else:
        form = EnterProfInfo()
    return render(request, 'index.html', {'form': form})

def results(request):
    return render(request, 'results.html')

# Create your views here.
