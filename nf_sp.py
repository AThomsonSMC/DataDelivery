'''
Find the shortest path to each node using a Topological Sorting algorithm.
'''

import nf_utils

def topological_sort(nodes, edges, node_bounds, edge_bounds, id):
    queued_nodes = []
    done_nodes = []
    best_parent = []
    
    for node in nodes:
        best_parent.append(-1)        #Initialize every node's parent to invalid -1
    
    cur_node = 0             #the id of the currently inspected node
    best_parent[0] = cur_node     #source node's parent is itself
    
    #Do this loop until the number of permanently labels nodes = number of nodes
    while len(done_nodes) < len(nodes):
        if cur_node == -1: raise Exception('Invalid node index')
        ob_edges = nf_utils.find_ob_edges(cur_node, node_bounds, edges, edge_bounds)   #Returns bounds of possible edge_ids for faster search.
        for edge in ob_edges:
            if edge[2] not in queued_nodes and edge[2] not in done_nodes:
                queued_nodes.append(edge[2])
            if (nodes[cur_node][1] + edge[4]) < nodes[edge[2]][1]:          #If new distance is better, update target node and best known parent
                nodes[edge[2]][1] = nodes[cur_node][1] + edge[4]
                best_parent[edge[2]] = cur_node
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