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
from nf_utils import write_file, INFINITY

# These determine the size of the graph
MIN_DC = 5
MAX_DC = 25
MIN_HUB = 50
MAX_HUB = 250
MIN_ISP = 500
MAX_ISP = 2500
MIN_USER = 5000
MAX_USER = 10000

#Assume data centers have a direct connection to the ISP Hubs - it's very fast and cheap to get a lot of data there.
#Capactiy comes from the ISP's ability to distribute that data.  Hubs are fairly well connected to their nodes,
#but the cost to get data to individual users can vary wildly.
MIN_DC_HUB_COST = 1
MAX_DC_HUB_COST = 5
MIN_HUB_ISP_COST = 1
MAX_HUB_ISP_COST = 20
MIN_ISP_USER_COST = 1
MAX_ISP_USER_COST = 100

MIN_DC_HUB_CAP = 10000
MAX_DC_HUB_CAP = 50000
MIN_HUB_ISP_CAP = 5000
MAX_HUB_ISP_CAP = 10000 
MIN_ISP_USER_CAP = 1
MAX_ISP_USER_CAP = 10

# Altering these will drastically effect m
MIN_DC_PER_HUB = 1
MAX_DC_PER_HUB = 3
MIN_HUB_PER_ISP = 2
MAX_HUB_PER_ISP = 5
MIN_ISP_PER_USER = 1
MAX_ISP_PER_USER = 5

#  All users demand at least 1 unit of flow, but will never reject excess - instead of having demands on nodes,
#   algorithm will check that every user gets at least one unit of flow.  This does not change the max-flow or min-cut.

#TODO: Move all these into statics.txt and read them in

def generate_network(timestamp):
    print '\nGenerating new network with id %s...\n' %timestamp
    this_nodes, this_node_bounds = generate_nodes()
    this_edges, this_edge_bounds = generate_edges(this_nodes, this_node_bounds)
    print 'Done generating network.'
    return this_nodes, this_edges, this_node_bounds, this_edge_bounds
    

def generate_nodes():
    nodes = []
    source_node = [0,0]             #source is always 0 distance from self
    nodes.append(source_node)
    num_dcs = randint(MIN_DC, MAX_DC)
    num_hub = randint(MIN_HUB, MAX_HUB)
    num_isp = randint(MIN_ISP, MAX_ISP)
    num_user = randint(MIN_USER, MAX_USER)
    node_bounds = [1]            #Because graph has multiple sets bipartite from eachother
                                     # use these bounds to know which "section" the node being examined is in.  Source node in it's own set.
    
    print 'Number of nodes:\n'
    print 'DCs: %s' %num_dcs
    print 'HUBs: %s' %num_hub
    print 'ISPs: %s' %num_isp
    print 'USERs: %s' %num_user

    #Initialize all nodes with INFINITY distance, we'll calc during the shortest path algorithm
    node_counter = 1
    for i in range(num_dcs):
        nodes.append([node_counter, INFINITY])
        node_counter += 1
    node_bounds.append(node_counter)
    for i in range(num_hub):
        nodes.append([node_counter, INFINITY])
        node_counter += 1
    node_bounds.append(node_counter)
    for i in range(num_isp):
        nodes.append([node_counter, INFINITY])
        node_counter += 1
    node_bounds.append(node_counter)
    for i in range(num_user):
        nodes.append([node_counter, INFINITY])
        node_counter += 1
    
    #TODO: write all_nodes out to nodes_[id].csv
    return nodes, node_bounds

def generate_edges(nodes, node_bounds):
    #Edges are of the form: [edge_id, tail_id, head_id, capacity, cost, flow]
    edge_list = []
    edge_id = 0
    edge_bounds = []            #Because graph has multiple bipartite sets, when searching for outbound edges from a node,
                                    # you know the min and max of possible edge_ids

    #Always infinite capacity, no cost edge from source to every DC
    for dc_node in nodes[1:node_bounds[1]]:
        edge_list.append([edge_id, 0, dc_node[0], INFINITY, 0, 0])
        edge_id += 1
    edge_bounds.append(edge_id)
    
    #For each hub, choose a number of DC's and make edges between these
    for hub_node in nodes[node_bounds[1]:node_bounds[2]]:
        num_dcs = randint(MIN_DC_PER_HUB, MAX_DC_PER_HUB)
        dcs = sample(range(1, node_bounds[1]), num_dcs)
        for dc in dcs:
            edge_list.append([edge_id, dc, hub_node[0], randint(MIN_DC_HUB_CAP, MAX_DC_HUB_CAP), randint(MIN_DC_HUB_COST, MAX_DC_HUB_COST), 0])
            edge_id += 1
    edge_bounds.append(edge_id)
    
    #Similarly, choose a number of Hubs for each ISP node to be connected to
    for isp_node in nodes[node_bounds[2]:node_bounds[3]]:
        num_hubs = randint(MIN_HUB_PER_ISP, MAX_HUB_PER_ISP)
        hubs = sample(range(node_bounds[1],node_bounds[2]), num_hubs)
        for hub in hubs:
            edge_list.append([edge_id, hub, isp_node[0], randint(MIN_HUB_ISP_CAP, MAX_HUB_ISP_CAP), randint(MIN_HUB_ISP_COST, MAX_HUB_ISP_COST), 0])
            edge_id += 1
    edge_bounds.append(edge_id)

    #Finally, choose a number of ISP Nodes for each user to be connected to
    for user_node in nodes[node_bounds[3]:]:
        num_isps = randint(MIN_ISP_PER_USER, MAX_ISP_PER_USER)
        isps = sample(range(node_bounds[2],node_bounds[3]), num_isps)
        for isp in isps:
            edge_list.append([edge_id, isp, user_node[0], randint(MIN_ISP_USER_CAP, MAX_HUB_ISP_CAP), randint(MIN_ISP_USER_COST, MAX_ISP_USER_COST), 0])
            edge_id += 1
            
    print 'Done creating edges, there are: %s' %edge_id
                
    return edge_list, edge_bounds


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