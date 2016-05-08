'''
Find the max-flow through the system - Use [Algorithm] to find the state that maximizes global flow while
satisfying demands.  By starting with a feasible network and then optimizing, we reduce runtime over starting with nothing
and incrementally pushing units of flow.
'''

import csv
import nf_utils
from nf_utils import INFINITY

test_nodes = [               #[node_id, demand]
  [0, 5],
  [1, 0],
  [2, 0],
  [3, 0],
  [4, 0],
  [5, 0],
  [6, 0],
  [7, -5]
]

test_edges = [               #[edge_id, tail_id, head_id, capacity, cost]
  [0, 0, 1, 5, 2],
  [1, 0, 4, 2, 4],
  [2, 1, 2, 8, 3],
  [3, 4, 2, 4, 4],
  [4, 4, 5, 3, 5],
  [5, 5, 6, 10, 2],
  [6, 6, 2, 4, 2],
  [7, 2, 3, 7, 1],
  [8, 6, 3, 6, 1],
  [9, 3, 7, 3, 2],
 [10, 6, 7, 7, 4]
]


def write_output(output, timestamp):
    with open('./io/max_flow_%s.csv' %timestamp, 'wb') as mffile:
        mfwriter = csv.writer(mffile, delimiter=',')
        for edge in output:
            mfwriter.writerow([edge, output[edge]])
    print 'Written to mf_%s.csv' %timestamp
    

def get_node_excess(node, ib_edges, ob_edges):
    #Takes in the graph and a node [id, +supply/-demand], and checks if current flow satisfies that node's demand.
    # Returns demand - cur_flow; negative means demand not being met, positive means node is over-supplied 
    demand = node[1]
    cur_flow = 0
    for edge in ib_edges:
        cur_flow += edge[5]
    for edge in ob_edges:
        cur_flow -= edge[5]
    return demand - cur_flow
    

def preflow_push(nodes, edges, node_bounds, edge_bounds, timestamp):
    #
    #  Use a preflow push algorithm to find the max-flow and min-cut
    #
    excess = []
    for node in nodes:
        excess.append(0)
    excess.append(0)        #Virtual sink node
    
    sink_distances = {}
    nodes.reverse()                     # we need to know User distances to find ISPs, need ISPs to find HUBs, etc.
    for node in nodes:
        # Figure out what section the current node is in and set edge searching bounds accordingly
        node_sec = 0
        ob_bounds = []
        for i in node_bounds:
            if node[0] >= i: node_sec += 1
        
        if node_sec == 4:
            sink_distances[node[0]] = 1
        elif node_sec == 3:
            ob_bounds = [edge_bounds[2],len(edges)]
        elif node_sec == 2:
            ob_bounds = [edge_bounds[1],edge_bounds[2]]
        elif node_sec == 1:
            ob_bounds = [edge_bounds[0],edge_bounds[1]]
        else:
            sink_distances[node[0]] = len(nodes)        # set distance of source node to n
        
        # Now iterate over outgoing edges to find best sink distance
        if node[0] not in sink_distances:
            best_d = INFINITY
            for edge in edges[ob_bounds[0]:ob_bounds[1]]:
                if edge[1] == node[0]:
                    pot = sink_distances[edge[2]] + edge[4]
                    if pot < best_d:
                        best_d = pot
            sink_distances[node[0]] = best_d
        
        if node[0] not in sink_distances:
            raise Exception('Did not find sink distance, something went wrong.')
    
    # Now that sink_distances have been found on all nodes, start pushing preflow
    res_edges = edges.copy()
    tot_edges = len(edges)
    for edge in edges:
        res_edges.append([tot_edges+edge[0],edge[2],edge[1],edge[3],edge[4],0])       #Initialize reverse edges with no flow
    
    
            
        
def mincost_experiment(nodes, edges, node_bounds, edge_bounds, timestamp):
    #
    #  !! This is an experimental algorithm that I tried to implement but couldn't convince myself that I could formally prove it is correct.
    #  !!  Instead, I implemented the standard preflow-push algorithm above for the sake of completing the project.
    #  !! I plan on refining this to see if I can get better performance by the nature of the topology of the graph.  What I'd like to show
    #  !!  is that I can get performance of O(m*(n_1^2+n_2^2+n_3^2+n_4^2)) << O(m*n^2) for some sets of n's, minimizing at n_i = .25*n
    #
    #  Use a modified preflow-push algorithm to find the min-cost flow.  Initialize the flow graph by pushing flow = min(demand, capacity)
    #  on ISP->User nodes.  Then calculate the total flow out of ISP nodes, and push flows from HUBs to satisfy (using lowest cost edges),
    #  and repeat from DCs to HUBs.  Once this preflow is found, iterate over user nodes to find excess flow (will never have shortage,
    #  generate_network checks for capacity feasibility before writing output).  Remove flow from highest cost edges until flow = demand.
    #                                                                             ^By highest cost, I'm using (edge_head_distance + cost)
    #  Once user demands are satisfied, repeat this process on ISPs and HUBs.  This will produce the min-cost flow that satisfies user demands.
    tot_flow = {}
    for edge in edges:
        flow[edge[0]] = 0
        
    for node in nodes[node_bounds[3]:]:
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                edge[5] += node[1]          #increment flow on edge by node demand
                if edge[5] > edge[3]: edge[5] = edge[3]     #if flow > cap, flow = cap

    # ISP->User edges all have flow, calc total flow through each ISP and send that flow through each incoming edge
    for node in nodes[node_bounds[2]:node_bounds[3]]:
        for edge in edges[edge_bounds[2]:]:
            if edge[1] == node[0]:
                node[1] += edge[5]          #increment "demand" on ISP node.  Will be set back to 0 once pushing that flow on inbound edges
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0                         #reset demand on ISP node to 0, it is transitionary
                
    #Repeat on HUBs
    for node in nodes[node_bounds[1]:node_bounds[2]]:
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[1] == node[0]:
                node[1] += edge[5]
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0
       
    #Finally repeat on DCs
    for node in nodes[node_bounds[0]:node_bounds[1]]:
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[1] == node[0]:
                node[1] += edge[5]
        for edge in edges[:edge_bounds[0]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0                 #DCs hace 0 demand, total demand is aggregated at source node
       
       
    # Network is now flooded, reduce flow into user nodes until demand is just satisfied, removing flow from most costly edges first
    for node in nodes[node_bounds[3]:]:
        ib_edges = []
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)   #Sort the inbound edges by their cost and then reverse for desc
        excess = get_node_excess(node, ib_edges, [])
        while excess > 0:
            ib_edges[0][5] = 0                              #Set most expensive inbound edge flow to 0
            excess = get_node_excess(node, ib_edges, [])    #Get node's new excess
            if excess < 0:
                ib_edges[0][5] += -1*excess                 #If removed too much flow, readd some to meet demand
            else:
                ib_edges.pop(0)                             #Remove edge from list of inbound edges
                
    # Users now have satisfied demands and no excess, remove excess on HUB->ISPs
    for node in nodes[node_bounds[2]:node_bounds[3]]:
        ib_edges = []
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    # Repeat for DC->HUB edges
    for node in nodes[node_bounds[1]:node_bounds[2]]:
        ib_edges = []
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    # Finally, repeat on source->DC edges
    for node in nodes[node_bounds[0]:node_bounds[1]]:
        ib_edges = []
        for edge in edges[:edge_bounds[0]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    print 'Min-cost flow found!'