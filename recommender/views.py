from django.shortcuts import render
from .forms import EnterProfInfo

import numpy as np

from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import networkx as nx
import pandas as pd

from recommender.build_graphs import get_coauthors_graph, get_topics_for_coauthor, get_author_id, save_author_id

def index(request):
    form = ""
    # if request.method == "POST":
    #     print("POST request method")
    #     if "search-prof" in request.POST:
    #         print("search-prof in request.POSt")
    #         form = EnterProfInfo(request.POST)
    #         author_id = request.POST.get("state")
    #         topic = request.POST.get("county")
    #         save_author_id(author_id)
    # else:
    form = EnterProfInfo()
    return render(request, 'index.html', {'form': form})

def results(request):
    #building graph
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    # x = np.arange(-2,1.5,.01)
    # y = np.sin(np.exp(2*x))
    # ax.plot(x, y)
    
    if request.method == "POST":
        form = EnterProfInfo(request.POST)
        author_id = request.POST.get("state")
        topic = request.POST.get("county")
        save_author_id(author_id)

    author_id = get_author_id()
    graph, coauthor_ids = get_coauthors_graph(author_id[0])
        #Bora's semantic scholar ID: 1734808354
        #Ziwei's semantic scholar ID: 9725200
    query_counter = 0
    topics = {}
    for coauthor_id, coauthor_name in coauthor_ids:
        topics[coauthor_name] = get_topics_for_coauthor(coauthor_id)
        query_counter += 1
        if (query_counter == 9):
            break
        
    pd.DataFrame(dict([(k, pd.Series(v)) for k, v in topics.items()])).to_csv("res.tsv", sep='\t')
    nx.draw(graph, ax=ax, with_labels=True)
        #if needed in requirements.txt:
        #decorator=4.4.2
    print(topics)

    response = HttpResponse(content_type='image/jpg') #changed to jpeg bc django doesn't like pngs. grr.
    canvas.print_jpg(response)
    return response

# Create your views here.
