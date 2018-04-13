#!/usr/bin/env python


"""Builds graph of users, IP and cookies and sessions"""

import md5
import csv
from datetime import datetime
import networkx as nx


input_file = "example/requests.csv"

max_label_len = 16
date_output_format = "%Y-%m-%d %H:%M:%S"
date_input_format = "%Y-%m-%d %H:%M:%S"


# -----------------------------------------------------------------------

def shorten_label(label):
    if len(label) > max_label_len:
        c = md5.new()
        c.update(label)
        return "%s... (%s)" % (label[:6], c.hexdigest()[-4:])
    else:
        return label


graph = nx.MultiDiGraph()


requests = csv.reader(open(input_file, "r"), delimiter=";")
header = requests.next()

dataset = list()

for row in requests:
    if len(row) < 1:
        continue

    data = dict()
    for i, label in enumerate(header):
        if label != "time":
            data[label] = shorten_label(row[i])
            data[label+"_full"] = row[i]
        else:
            data[label] = row[i]
    data["time"] = datetime.strftime(
        datetime.strptime(data["time"], date_input_format),
        date_output_format)
    dataset.append(data)

time_end = max(map(lambda x: x["time"], dataset))

for data in dataset:
    if data["ip"] != "-" and data["account"] != "-":
        if data["ip"] not in graph:
            graph.add_node(data["ip"], type="ip", label_full=data["ip_full"],
                           time_start=data["time"], time_end=time_end)
        if data["account"] not in graph:
            graph.add_node(data["account"], type="account",
                           label_full=data["account_full"],
                           time_start=data["time"], time_end=time_end)
        graph.add_edge(data["ip"], data["account"])
        print "%s -()-> %s" % (data["ip"], data["account"])

    if data["utma"] != "-" and data["account"] != "-":
        if data["utma"] not in graph:
            graph.add_node(data["utma"], type="cookie",
                           label_full=data["utma_full"],
                           time_start=data["time"], time_end=time_end)
        graph.add_edge(data["account"], data["utma"])
        print "%s -(cookie)-> %s" % (data["account"], data["utma"])

    if data["session"] != "-" and data["account"] != "-":
        if data["session"] not in graph:
            graph.add_node(data["session"], type="session",
                           label_full=data["session_full"],
                           time_start=data["time"], time_end=time_end)
        graph.add_edge(data["account"], data["session"])
        print "%s -(session)-> %s" % (data["account"], data["session"])

nx.write_gexf(graph, "graph.gexf")
