'''
Find the max-flow through the system - Use [Algorithm] to find the state that maximizes global flow while
satisfying demands.  By starting with a feasible network and then optimizing, we reduce runtime over starting with nothing
and incrementally pushing units of flow.
'''

import csv
import nf_utils

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
    

def check_demand(node, node_bounds, edges, edge_bounds, tot_edges):
    #Takes in the graph and a node [id, +supply/-demand], and checks if current flow satisfies that node's demand.
    # Returns demand - cur_flow; negative means demand not being met, positive means node is over-supplied 
    demand = node[1]
    cur_flow = 0
    if demand == 0:
        return 0
    if demand < 0:
        search_bounds = nf_utils.find_inbound_edges(node[0], node_bounds, edge_bounds, tot_edges)
        for edge in edges[search_bounds[0]:search_bounds[1]]:
            if edge[2] == node[0]:
                cur_flow += edges[5]
        return demand + cur_flow == 0
    elif demand > 0:
        search_bounds = nf_utils.find_outbound_edges(node[0], node_bounds, edge_bounds, tot_edges)
        for edge in edges[search_bounds[0]:search_bounds[1]]:
            if edge[1] == node[0]:
                cur_flow -= edges[5]
        return demand + cur_flow == 0
    else:
        # ????? Something went very wrong
        raise Exception
        
        
def max_flow(nodes, edges, node_bounds, edge_bounds, timestamp):
    #  Use a preflow-push algorithm to find the min-cost flow.  Initialize the flow graph by pushing flow = capacity on ISP->User nodes
    #  Then calculate the total flow out of ISP nodes, and push flows from HUBs to satisfy (using lowest cost edges), and repeat from DCs to HUBs.
    #  Once this preflow is found, loop over user nodes to find excess flow (will never have shortage, generate_network checks for
    #  feasibility before writing output).  Remove flow from highest cost edges until flow = demand.  Once user demands are satisfied,
    #  repeat this process on ISPs and HUBs.  This will produce the min-cost flow that satisfies user demands.
    flow = {}
    for edge in edges:
        flow[edge[0]] = 0
    user_edge_search_bounds = nf_utils.find_inbound_edges(nodes[-1][0])    #The last node will always be a user node.
    for node in nodes[node_bounds[2]:]: