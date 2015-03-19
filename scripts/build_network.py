#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import csv, json
import networkx as nx
from networkx.readwrite import json_graph

class Graph(nx.Graph):

    def write_graph_in_format(self, filerootname, fileformat='gexf'):
        fileformat = fileformat.lower()
        filename = "%s.%s" % (filerootname.replace(" ", "_"), fileformat)
        if fileformat == 'json':
            with open(filename, 'w') as f:
                json.dump(json_graph.node_link_data(self), f)
        elif fileformat == 'net':
            nx.write_pajek(self, filename)
        else:
            nx.write_gexf(self, filename)

    def add_node(self, node, **kwargs):
        if self.has_node(node):
            self.node[node]['occurences'] += 1
        else:
            nx.Graph.add_node(self, node, occurences=1)
        for key, value in kwargs.items():
            try:
                value = float(value)
            except ValueError:
                pass
            if key in self.node[node] and \
              isinstance(value, float) and isinstance(self.node[node][key], float):
                self.node[node][key] += value
            elif key not in self.node[node]:
                self.node[node][key] = value
        if "label" not in self[node]:
            self.node[node]["label"] = node

    def add_edge(self, node1, node2, weight=1):
        if self.has_edge(node1, node2):
            self[node1][node2]['weight'] += weight
        else:
            nx.Graph.add_edge(self, node1, node2, weight=weight)


if __name__ == "__main__":
    rows = medecins = 0
    G = Graph()
    links = {}
    rootpath = os.path.join("data", "public")
    with open(os.path.join(rootpath, "sunshine.anonymes.csv")) as f:
        for row in csv.DictReader(f):
            row["LABO"] = row["LABO"].decode('utf8')
            if rows and rows % 10000 == 0:
                print >> sys.stderr, rows, len(G.nodes()), medecins, len(G.edges())
            rows += 1
            G.add_node(row["LABO"], montants=row["DECL_AVANT_MONTANT"])
            if row["BENEF_PS_ID"] in links:
                if row["LABO"] not in links[row["BENEF_PS_ID"]]:
                    for lab in links[row["BENEF_PS_ID"]]:
                        G.add_edge(row["LABO"], lab)
                    links[row["BENEF_PS_ID"]].append(row["LABO"])
            else:
                medecins += 1
                links[row["BENEF_PS_ID"]] = [row["LABO"]]

    for n in G.copy().nodes_iter():
        if not G.degree(n):
           G.remove_node(n)

    filename = os.path.join(rootpath, "labos%s")
    with open(filename % ".nodes.csv", 'w') as f:
        print >> f, "label,montants,occurences"
        for n in G.nodes_iter():
            print >> f, ("%s,%s,%s" % (G.node[n]["label"], str(G.node[n]["montants"]), str(G.node[n]["occurences"]))).encode('utf8')
    with open(filename % ".edges.csv", 'w') as f:
        print >> f, "node1,node2,weight"
        for n1, n2, w in G.edges_iter(data=True):
            print >> f, ("%s,%s,%s" % (n1, n2, str(w["weight"]))).encode('utf8')
    G.write_graph_in_format(filename % ".network", "net")
    #G.write_graph_in_format(filename % ".network", "json")
    G.write_graph_in_format(filename % ".network", "gexf")

