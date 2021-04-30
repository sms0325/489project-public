import itertools
import requests
import pandas as pd
import networkx as nx
from collections import Counter
from functools import reduce
import operator

YEAR = 2021

def save_coauthor_id(author_id):
    filename = input(author_id)
    with open("id.txt", "w") as f:
        f.write(input())

def get_coauthor_id():
    with open('id.txt') as f:
        coauthor_id = f.readlines()
    return coauthor_id

def get_coauthors_graph(author_id):
    # Get the original author's profile
    print(author_id)
    query = requests.get(f"https://api.semanticscholar.org/v1/author/{author_id}").json()
    #print(query)
    original_author = {'authorId': query['authorId'], 'name': query['name'], 'url': query['url']}
    # Make a DataFrame of the original author's papers
    papers = pd.DataFrame(query['papers'])
    # Query for the actual papers
    specific_papers = list(
        map(lambda url: requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{url}"), papers['url']))
    # Convert to a list of JSONs
    specific_paper_jsons = list(map(lambda x: x.json(), specific_papers))
    # Get coauthors
    coauthors = [specific_paper_json['authors'] for specific_paper_json in specific_paper_jsons]
    coauthors = list(itertools.chain.from_iterable(coauthors))
    edge_list = [(original_author['name'], coauthor['name']) for coauthor in coauthors]
    edge_list_with_ids = [(original_author['authorId'], coauthor['authorId']) for coauthor in coauthors]
    G = nx.Graph(edge_list)
    return G, list(zip(list(map(lambda x: x[1], edge_list_with_ids)), list(map(lambda x: x[1], edge_list))))


def get_topics_for_coauthor(author_id):
    #print(author_id)
    query = requests.get(f"https://api.semanticscholar.org/v1/author/{author_id}").json()
    recent_papers = list(filter(lambda x: (x['year'] if x['year'] is not None else 0) >= YEAR, query['papers']))
    paper_queries = [requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{x['url']}").json() for x in
                     recent_papers]
    topics = [n['topics'] for n in paper_queries]
    return Counter([x['topic'] for x in reduce(operator.concat, topics)]).most_common()


def get_coauthors_as_edge_list(author_id):
    # Get the original author's profile
    query = requests.get(f"https://api.semanticscholar.org/v1/author/{author_id}").json()
    original_author = {'authorId': query['authorId'], 'name': query['name'], 'url': query['url']}
    # Make a DataFrame of the original author's papers
    papers = pd.DataFrame(query['papers'])
    recent_papers = papers[papers['year'] >= YEAR]
    print(recent_papers['year'])
    # Query for the actual papers where year >= YEAR
    specific_papers = list(
        map(lambda url: requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{url}"), recent_papers['url']))
    # Convert to a list of JSONs
    specific_paper_jsons = list(map(lambda x: x.json(), specific_papers))
    # Get coauthors
    coauthors = [specific_paper_json['authors'] for specific_paper_json in specific_paper_jsons]
    coauthors = list(itertools.chain.from_iterable(coauthors))
    edge_list = [(original_author['name'], coauthor['name']) for coauthor in coauthors]
    edge_list_with_ids = [(original_author['authorId'], coauthor['authorId']) for coauthor in coauthors]
    return edge_list, edge_list_with_ids

# edge_list, edge_list_with_ids = get_coauthors_as_edge_list("1697232")
# print(edge_list)
# print(edge_list_with_ids)
