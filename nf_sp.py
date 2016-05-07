'''
Find the shortest path to each node.  Using Djikstra's algorithm.
'''

import nf_utils
from nf_generate_network import INFINITY

#This is test data for a small, acyclic graph
test_nodes = [               #[node_id, distance]
  [0, 0],
  [1, 0],
  [2, 0],
  [3, 0],
  [4, 0],
  [5, 0],
  [6, 0],
  [7, 0]
]

test_edges = [               #[edge_id, tail_id, head_id, capacity, cost, flow (unused here)]
  [0, 0, 1, 99],
  [1, 0, 4, 99],
  [2, 1, 2, 99],
  [3, 1, 5, 99],
  [4, 4, 5, 99],
  [5, 5, 2, 99],
  [6, 5, 6, 99],
  [7, 2, 6, 99],
  [8, 6, 3, 99],
  [9, 6, 7, 99],
 [10, 3, 7, 99]
]    
    
def topological_sort(nodes, edges, node_bounds, edge_bounds, id):
    queued_nodes = []
    done_nodes = []
    best_parent = {}
    
    for node in nodes:
        best_parent[node[0]] = -1        #Initialize every node's parent to invalid -1
    
    cur_node = 0             #the id of the currently inspected node
    best_parent[0] = cur_node     #source node's parent is itself
    
    #Do this loop until the number of permanently labels nodes = number of nodes
    while len(done_nodes) < len(nodes):
        if cur_node == -1: raise Exception('Invalid node index')
        search_bounds = nf_utils.find_outbound_edges(cur_node, node_bounds, edge_bounds, len(edges))   #Returns bounds of possible edge_ids for faster search.
        for edge in edges[search_bounds[0]:search_bounds[1]]:
            if edge[1] == cur_node:
                if edge[2] not in queued_nodes and edge[2] not in done_nodes:
                    queued_nodes.append(edge[2])
                if (nodes[cur_node][1] + edge[4]) < nodes[edge[2]][1]:
                    nodes[edge[2]][1] = nodes[cur_node][1] + edge[4]
                    best_parent[edge[2]] = edge[1]
        done_nodes.append(cur_node)
        try:
            cur_node = queued_nodes.pop(0)      #Set cur_node to first element and then remove node from queue
        except IndexError:
            cur_node = -1               #Queue is empty, set cur_node to invalid id.  Either done or something went wrong.
    
    print 'Done finding shortest paths, writing to disk.'
    nf_utils.write_file(nodes, 'nodes', id)      #Wait to write nodes until now for distances
    print 'Nodes written to: nodes_%s.csv' %id
    
    sp_out = []
    for node in nodes:
        sp_out.append([node[0], best_parent[node[0]]])
    nf_utils.write_file(sp_out, 'sp', id)
    print 'Shortest paths written to: sp_%s.csv' %id
    
        
if __name__ == "__main__":
    topological_sort(test_nodes, test_edges, [999,999,999], [999,999,999], 'TEST123')