'''
Utility methods go here.
'''

import csv


INFINITY = 999999999                #Effectively infinite, but prints to csv better

#Node sections:
    #0 = source
    #1 = DCs
    #2 = HUBs
    #3 = ISPs
    #4 = Users
    #5 = sink
    
#Edge bounds:
    # [:eb[0]] = source->DCs
    # [eb[0]:eb[1]] = DCs->HUBs
    # [eb[1]:eb[2]] = HUBs->ISPs
    # [eb[2]:eb[3]] = ISPs->Users
    # [eb[3]:] = Users->sink
    
def get_node_section(node_id, node_bounds):
    node_sec = 0
    for bound in node_bounds:
        if node_id >= bound: node_sec += 1
    return node_sec
    
def get_ij_edge(i, j, edges):
    for edge in edges:
        if edge[1] == i and edge[2] == j:
            return edge
    #No i,j edge
    return []
    

#Determine which set the node is in and then define the bounds to search for outbound edges
def find_ob_edges(node_id, node_bounds, edges, edge_bounds):
    node_section = get_node_section(node_id, node_bounds)
    if node_section == 5: 
        return []     #sink has no outbound edges
    elif node_section == 4:
        for edge in edges[edge_bounds[3]:]:
            if edge[1] == node_id: return [edge] 
    elif node_section == 0:
        return edges[:edge_bounds[0]]   #source has all source->DC edges outbound
    else:
        ob_edges = []
        for edge in edges[edge_bounds[node_section-1]: edge_bounds[node_section]]:
            if edge[1] == node_id:
                ob_edges.append(edge)
        return ob_edges
    
def find_ib_edges(node_id, node_bounds, edges, edge_bounds):
    node_section = get_node_section(node_id, node_bounds)
    if node_section == 5:
        return edges[edge_bounds[3]:]       #sink node has all user->sink edges inbound
    elif node_section == 0:
        return []   # source node has no inbound edges
    elif node_section == 1:
        return [edges[node_id-1]]   # DC's always have edge_id = (node_id - 1) inbound
    else:
        ib_edges = []
        for edge in edges[edge_bounds[node_section-2]: edge_bounds[node_section-1]]:
            if edge[2] == node_id:
                ib_edges.append(edge)
        return ib_edges
    
    
def write_file(data_list, name, id):
    with open('./io/%s_%s.csv' %(name, id), 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        for data in data_list:
            writer.writerow(data)