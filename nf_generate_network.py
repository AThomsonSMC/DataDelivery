'''
Generate the topology of the network - composed of 'DataCenter's, 'ISPHub's, 'ISPNode's, and 'User's.  Each of these
types of nodes are bipartite to each other.  Flow (representing data) starts at the DataCenters, and must fulfill the
demand of all the Users.

For the sake of simplifying the model, DataCenters are directly connected to ISPHubs which
are connected to the ISPNodes, then finally reaches Users.  ISPHubs and ISPNodes have 0 demand, Users will each have a
negative demand.  A trivial node will be the parent of all DataCenters, with a positive demand equal to the sum of the
Users' demands.
'''

from random import randint, sample

#define statics
MIN_DC = 5
MAX_DC = 10
MIN_HUB = 10
MAX_HUB = 50
MIN_ISP = 100
MAX_ISP = 1000
MIN_USER = 10000
MAX_USER = 50000

#Assume data centers have a direct connection to the ISP Hubs - it's very fast and cheap to get unlimited data there.
#Capactiy comes from the ISP's ability to distribute that data.  Hubs are fairly well connected to their nodes,
#but the cost to get data to individual users can vary wildly.
MIN_DC_HUB_COST = 1
MAX_DC_HUB_COST = 5
MIN_HUB_ISP_COST = 1
MAX_HUB_ISP_COST = 20
MIN_ISP_USER_COST = 1
MAX_ISP_USER_COST = 100

DC_HUB_CAP = 999999999          #Effectively infinity, but prints into a csv better
MIN_HUB_ISP_CAP = 1000
MAX_HUB_ISP_CAP = 5000
MIN_USER_DEMAND = 1
MAX_USER_DEMAND = 10
ISP_USER_CAP = MAX_USER_DEMAND      #flow to individual users is decided by their demand, not capacity
                                    #in reality, demand is often limited by capacity, but behavior is same for the model
                                    #storing data this way allows for faster lookups since n < m

MIN_DC_PER_HUB = 1
MAX_DC_PER_HUB = 3
MIN_HUB_PER_ISP = 2
MAX_HUB_PER_ISP = 10
MIN_ISP_PER_USER = 1
MAX_ISP_PER_USER = 10

#TODO: Move all these into statics.txt and read them in

def generate_nodes():
    dc_nodes, hub_nodes, isp_nodes, user_nodes = [], [], [], []
    source_node = [0,0]             #initialize demand to 0, set to balance total user demand once generated
    num_dcs = randint(MIN_DC, MAX_DC)
    num_hub = randint(MIN_HUB, MAX_HUB)
    num_isp = randint(MIN_ISP, MAX_ISP)
    num_user = randint(MIN_USER, MAX_USER)

    node_counter = 1
    for i in range(num_dcs):
        dc_nodes.append([node_counter, 0])
        node_counter += 1
    for i in range(num_hub):
        hub_nodes.append([node_counter, 0])
        node_counter += 1
    for i in range(num_isp):
        isp_nodes.append([node_counter, 0])
        node_counter += 1

    total_demand = 0
    for i in range(num_user):
        user_demand = randint(MIN_USER_DEMAND, MAX_USER_DEMAND)
        user_nodes.append([node_counter, (user_demand * -1)])       #Negative for demand
        total_demand += user_demand
        node_counter += 1

    source_node[1] = total_demand

    all_nodes = source_node + dc_nodes + hub_nodes + isp_nodes + user_nodes

    #TODO: write all_nodes out to nodes_[id].csv
    return source_node, dc_nodes, hub_nodes, isp_nodes, user_nodes

def generate_edges(node_lists):
    #Infinite capacity is represented by 999999999.

    edge_list = []
    edge_id = 0

    #Always infinite capacity edge from source to every DC
    for dc_node in node_lists[1]:
        edge_list.append([edge_id, 0, dc_node[0], 999999999, 0])
        edge_id += 1

    #For each hub, choose a number of DC's and make infinite capacity edges between these
    for hub_node in node_lists[2]:
        num_dcs = randint(MIN_DC_PER_HUB, MAX_DC_PER_HUB)
        dcs = sample(range(node_lists[1][0][0], node_lists[1][-1][0] + 1), num_dcs)
        for dc in dcs:
            edge_list.append([edge_id, dc, hub_node[0], 999999999, randint(MIN_DC_HUB_COST, MAX_DC_HUB_COST)])
            edge_id += 1

    #Similarly, choose a number of Hubs for each ISP node to be connected to
    for isp_node in node_lists[3]:
        num_hubs = randint(MIN_HUB_PER_ISP, MAX_HUB_PER_ISP)
        hubs = sample(range(node_lists[2][0][0], node_lists[2][-1][0] + 1), num_hubs)
        for hub in hubs:
            edge_list.append([edge_id, hub, isp_node[0], 999999999, randint(MIN_HUB_ISP_COST, MAX_HUB_ISP_COST)])
            edge_id += 1

    #Similarly, choose a number of ISP Nodes for each user to be connected to
    for user_node in node_lists[4]:
        num_isps = randint(MIN_ISP_PER_USER, MAX_ISP_PER_USER)
        isps = sample(range(node_lists[3][0][0], node_lists[3][-1][0] + 1), num_isps)
        for isp in isps:
            edge_list.append([edge_id, isp, user_node[0], 999999999, randint(MIN_ISP_USER_COST, MAX_ISP_USER_COST)])
            edge_id += 1


    #TODO: Write edge data out to file