import itertools
import requests
import pandas as pd
import networkx as nx
import operator
from functools import reduce
from collections import Counter

YEAR = 2021

def get_topics_for_coauthor(author_id):
    print(author_id)
    query = requests.get(f"https://api.semanticscholar.org/v1/author/{author_id}").json()
    recent_papers = list(filter(lambda x: (x['year'] if x['year'] is not None else 0) >= YEAR, query['papers']))
    paper_queries = [requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{x['url']}").json() for x in recent_papers]
    topics = [n['topics'] for n in paper_queries]
    return Counter([x['topic'] for x in reduce(operator.concat, topics)]).most_common()

def get_coauthors_as_edge_list(author_id):
    # Get the original author's profile
    query = requests.get(f"https://api.semanticscholar.org/v1/author/{author_id}").json()
    original_author = {'authorId': query['authorId'], 'name': query['name'], 'url': query['url']}
    # Make a DataFrame of the original author's papers
    papers = pd.DataFrame(query['papers'])
    recent_papers = papers[papers['year'] >= YEAR]
    # Query for the actual papers where year >= YEAR
    specific_papers = list(map(lambda url: requests.get(f"https://api.semanticscholar.org/v1/paper/URL:{url}"), recent_papers['url']))
    # Convert to a list of JSONs
    specific_paper_jsons = list(map(lambda x: x.json(), specific_papers))
    # Get coauthors
    coauthors = [specific_paper_json['authors'] for specific_paper_json in specific_paper_jsons]
    coauthors = list(itertools.chain.from_iterable(coauthors))
    edge_list = [(original_author['name'], coauthor['name']) for coauthor in coauthors]
    edge_list_with_ids = [(original_author['authorId'], coauthor['authorId']) for coauthor in coauthors]
    return edge_list, edge_list_with_ids

def get_recs(id):
    _, edge_list_with_ids = get_coauthors_as_edge_list(id)
    coauthors = list(pd.Series([x[1] for x in edge_list_with_ids if x[1] is not None]).unique())
    coauthor_topics = {x: get_topics_for_coauthor(x) for x in coauthors}
    return coauthor_topics