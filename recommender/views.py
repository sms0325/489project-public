from django.shortcuts import render
from .forms import EnterProfInfo

import numpy as np

from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import networkx as nx
import pandas as pd

import io

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
    ax = fig.add_subplot(111)
    canvas = FigureCanvas(fig)
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
    buf = io.BytesIO()
    canvas.print_png(buf)
    #plt.savefig(buf, format='jpg')
    #plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    fig.clear()
    response['Content-Length'] = str(len(response.content))
    return response

# Create your views here.
