'''
Once the max-flow has been found, determine the dual min-cut.  This will usually be all of the edges splitting two of the
partites in the network, but not necessarily always.  Because of the graph topology, the min-cut will give us a good understanding of
the physical representation of the network's bottleneck.
'''

import nf_utils

def min_cut(nodes, edges, node_bounds, edge_bounds, timestamp):
    # First, create res_edges list with cap* = cap - flow
    res_edges = []
    for edge in edges:
        res_edges.append([edge[0],edge[1],edge[2],edge[3]-edge[5]])
    
    # Initialize list of nodes reachable from source and sink
    n1, n2 = [0], []
    found_nodes = [0]
    while len(found_nodes) > 0:
        cur_node = found_nodes.pop(0)
        n1.append(cur_node)
        ob_edges = nf_utils.find_ob_edges(cur_node, node_bounds, res_edges, edge_bounds)
        for edge in ob_edges:
            if edge[3] == 0:
                continue
            else:
                if edge[2] not in n1 and edge[2] not in found_nodes:
                    found_nodes.append(edge[2])
                    
    # We have found n1.  By definition of a cut, we know any node not in n1 must be in n2
    for node in nodes:
        if node[0] not in n1:
            n2.append(node[0])
            
    #print 'N: ' + str(n1)
    #print 'N_: ' + str(n2)
            
    # Now find all the edges between n1 and n2 and write that to file.
    output = []
    for edge in edges:
        if (edge[1] in n1 and edge[2] in n2) or (edge[1] in n2 and edge[2] in n1):      # By graph topology, not sure if second case is possible?
            output.append([edge[0],1])
        else:
            output.append([edge[0],0])
            
    print 'Min-Cut has been found!  Written to min_cut_%s.csv' %timestamp
    nf_utils.write_file(output, "min_cut", timestamp)
                