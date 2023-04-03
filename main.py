from neo4j import GraphDatabase
import requests
import random
from urllib.request import urlopen
from lxml.html import parse
from bs4 import BeautifulSoup
lin = []

name = ""


def get_wikipedia_links():

    query = name.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit=1000000000&offset=0&ns0=1&search={query}"
    response = requests.get(search_url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if href.startswith("/wiki/"):
            title = link.get("title")
            if title:
                lin.append(title)


class Neo4jGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_name_nodes(self, links):
        with self.driver.session() as session:
            # Generate label name from name variable
            label_name = name.replace(" ", "")
            for link in links:
                session.run("MERGE (:{label} {{link: $link}})".format(
                    label=label_name), link=link)
            nodes = session.run(
                "MATCH (n:{label}) RETURN n.link as link".format(label=label_name))
            nodes = [record["link"] for record in nodes]
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if random.random() < 0.5:
                        session.run("MATCH (n1:{label} {{link: $link1}}), (n2:{label} {{link: $link2}}) "
                                    "MERGE (n1)-[:KNOWS]->(n2)".format(label=label_name), link1=nodes[i], link2=nodes[j])


def run1():
    print(name)
    get_wikipedia_links()

    graph = Neo4jGraph("bolt://localhost:7687", "neo4j", "Pooja@4749")
    graph.create_name_nodes(lin)
    print("sucess")
    graph.close()
