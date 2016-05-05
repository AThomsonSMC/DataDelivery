'''
Generate the topology of the network - composed of 'DataCenter's, 'ISPHub's, 'ISPNode's, and 'User's.  Each of these
types of nodes are bipartite to each other.  Flow (representing data) starts at the DataCenters, and must fulfill the
demand of all the Users.

For the sake of simplifying the model, DataCenters are directly connected to ISPHubs which
are connected to the ISPNodes, then finally reaches Users.  ISPHubs and ISPNodes have 0 demand, Users will each have a
negative demand.  A trivial node will be the parent of all DataCenters, with a positive demand equal to the sum of the
Users' demands.
'''

from random import randint, sample  #randit(a,b) returns random integer in [a,b]; sample(a,b,k) chooses k unique integers in [a,b] 
from time import time               #Gives the number of seconds since epoch
import csv

INFINITY = 999999999                #Effectively infinite, but prints to csv better


#define statics
MIN_DC = 5
MAX_DC = 25
MIN_HUB = 50
MAX_HUB = 250
MIN_ISP = 500
MAX_ISP = 2500
MIN_USER = 5000
MAX_USER = 10000

#Assume data centers have a direct connection to the ISP Hubs - it's very fast and cheap to get unlimited data there.
#Capactiy comes from the ISP's ability to distribute that data.  Hubs are fairly well connected to their nodes,
#but the cost to get data to individual users can vary wildly.
MIN_DC_HUB_COST = 1
MAX_DC_HUB_COST = 5
MIN_HUB_ISP_COST = 1
MAX_HUB_ISP_COST = 20
MIN_ISP_USER_COST = 1
MAX_ISP_USER_COST = 100

DC_HUB_CAP = INFINITY
MIN_HUB_ISP_CAP = 5000
MAX_HUB_ISP_CAP = 20000
MIN_USER_DEMAND = 1
MAX_USER_DEMAND = 10
ISP_USER_CAP = MAX_USER_DEMAND      #flow to individual users is decided by their demand, not capacity
                                    #in reality, demand is often limited by capacity, but behavior is same for the model

MIN_DC_PER_HUB = 1
MAX_DC_PER_HUB = 3
MIN_HUB_PER_ISP = 2
MAX_HUB_PER_ISP = 10
MIN_ISP_PER_USER = 1
MAX_ISP_PER_USER = 5

#TODO: Move all these into statics.txt and read them in

def generate_network(timestamp):
    print '\nGenerating new network with id %s...\n' %timestamp
    new_nodes = generate_nodes()
    node_boundaries = new_nodes[6]
    new_edges, edge_boundaries = generate_edges(new_nodes)
    print 'Number of edges: %s' %len(new_edges)
    #TODO: Check network feasibility, rerun until it is feasible
    write_files(new_nodes, new_edges, timestamp)
    print 'Done generating network.  Saved as "nodes_%s" and "edges_%s".' %(timestamp, timestamp)
    return new_nodes[5], new_edges, node_boundaries, edge_boundaries
    

def generate_nodes():
    dc_nodes, hub_nodes, isp_nodes, user_nodes = [], [], [], []
    source_node = [0,0]             #initialize demand to 0, set to balance total user demand once generated
    num_dcs = randint(MIN_DC, MAX_DC)
    num_hub = randint(MIN_HUB, MAX_HUB)
    num_isp = randint(MIN_ISP, MAX_ISP)
    num_user = randint(MIN_USER, MAX_USER)
    node_boundaries = [1]            #Because graph has multiple sets bipartite from eachother
                                     # use these bounds to know which "section" the node being examined is in.  Source node in it's own set.
    
    print 'Number of nodes:\n'
    print 'DCs: %s' %num_dcs
    print 'HUBs: %s' %num_hub
    print 'ISPs: %s' %num_isp
    print 'USERs: %s' %num_user

    node_counter = 1
    for i in range(num_dcs):
        dc_nodes.append([node_counter, 0])
        node_counter += 1
    node_boundaries.append(node_counter)
    for i in range(num_hub):
        hub_nodes.append([node_counter, 0])
        node_counter += 1
    node_boundaries.append(node_counter)
    for i in range(num_isp):
        isp_nodes.append([node_counter, 0])
        node_counter += 1
    node_boundaries.append(node_counter)

    total_demand = 0
    for i in range(num_user):
        user_demand = randint(MIN_USER_DEMAND, MAX_USER_DEMAND)
        user_nodes.append([node_counter, (user_demand * -1)])       #Negative for demand
        total_demand += user_demand
        node_counter += 1

    source_node[1] = total_demand

    all_nodes = []
    all_nodes.append(source_node)
    for node in dc_nodes:
        all_nodes.append(node)
    for node in hub_nodes:
        all_nodes.append(node)
    for node in isp_nodes:
        all_nodes.append(node)
    for node in user_nodes:
        all_nodes.append(node)

    #TODO: write all_nodes out to nodes_[id].csv
    return source_node, dc_nodes, hub_nodes, isp_nodes, user_nodes, all_nodes, node_boundaries

def generate_edges(node_lists):
    
    #Edges are of the form: [edge_id, tail_id, head_id, capacity, cost]
    edge_list = []
    edge_id = 0
    edge_boundaries = []            #Because graph has multiple bipartite sets, when searching for outbound edges from a node,
                                    # you know the min and max of possible edge_ids

    #Always infinite capacity edge from source to every DC
    for dc_node in node_lists[1]:
        edge_list.append([edge_id, 0, dc_node[0], INFINITY, 0])
        edge_id += 1
    edge_boundaries.append(edge_id)

    #For each hub, choose a number of DC's and make infinite capacity edges between these
    for hub_node in node_lists[2]:
        num_dcs = randint(MIN_DC_PER_HUB, MAX_DC_PER_HUB)
        dcs = sample(range(node_lists[1][0][0], node_lists[1][-1][0] + 1), num_dcs)
        for dc in dcs:
            edge_list.append([edge_id, dc, hub_node[0], INFINITY, randint(MIN_DC_HUB_COST, MAX_DC_HUB_COST)])
            edge_id += 1
    edge_boundaries.append(edge_id)

    #Similarly, choose a number of Hubs for each ISP node to be connected to
    for isp_node in node_lists[3]:
        num_hubs = randint(MIN_HUB_PER_ISP, MAX_HUB_PER_ISP)
        hubs = sample(range(node_lists[2][0][0], node_lists[2][-1][0] + 1), num_hubs)
        for hub in hubs:
            edge_list.append([edge_id, hub, isp_node[0], INFINITY, randint(MIN_HUB_ISP_COST, MAX_HUB_ISP_COST)])
            edge_id += 1
    edge_boundaries.append(edge_id)

    #Similarly, choose a number of ISP Nodes for each user to be connected to
    for user_node in node_lists[4]:
        num_isps = randint(MIN_ISP_PER_USER, MAX_ISP_PER_USER)
        isps = sample(range(node_lists[3][0][0], node_lists[3][-1][0] + 1), num_isps)
        for isp in isps:
            edge_list.append([edge_id, isp, user_node[0], INFINITY, randint(MIN_ISP_USER_COST, MAX_ISP_USER_COST)])
            edge_id += 1
    
    return edge_list, edge_boundaries


def write_files(nodes_list, edge_list, timestamp):
    with open('./io/nodes_%s.csv' %timestamp, 'wb') as nodefile:
        nodewriter = csv.writer(nodefile, delimiter=',')
        for nodes in nodes_list:
            nodewriter.writerow(nodes)
    with open('./io/edges_%s.csv' %timestamp, 'wb') as edgefile:
        edgewriter = csv.writer(edgefile, delimiter=',')
        for edge in edge_list:
            edgewriter.writerow(edge)


if __name__ == '__main__':
    TIMESTAMP = int(time())
    run_nodes = generate_nodes(TIMESTAMP)
    print 'ID: %s' %TIMESTAMP
    print 'Number of nodes:\n'
    print 'DCs: %s' %len(run_nodes[1])
    print 'HUBs: %s' %len(run_nodes[2])
    print 'ISPs: %s' %len(run_nodes[3])
    print 'USERs: %s' %len(run_nodes[4])
    run_edges = generate_edges(run_nodes)
    print 'Number of edges: %s' %len(run_edges)
    write_files(run_nodes, run_edges, TIMESTAMP)