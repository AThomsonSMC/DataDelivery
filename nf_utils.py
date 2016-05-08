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

#Determine which set the node is in and then define the bounds to search for outbound edges
def find_outbound_edges(node_id, node_bounds, edge_bounds, tot_edges):
    node_section = 0
    for bound in node_bounds:
        if bound <= node_id:
            node_section += 1
    if node_section == 4: return [-1,-1]   # node_section = 4 means we're examining users which have no outbound edges
    
    #Define the bounds of edge_ids to search for outbound edges, depends on "node_section" currently in
    if node_section == 0:
        search_bounds = [0,edge_bounds[0]]
    elif node_section == 3:
        search_bounds = [edge_bounds[2], tot_edges]
    else:
        search_bounds = [edge_bounds[node_section-1], edge_bounds[node_section]]
        
    return search_bounds
    
def find_inbound_edges(node_id, node_bounds, edge_bounds, tot_edges):
    node_section = 0
    for bound in node_bounds:
        if bound <= node_id:
            node_section += 1
    if node_section == 0: return [-1,-1]    # node_section = 0 means we're examining the source node which has no inbound edges
           
    #Define the bounds of edge_ids to search for outbound edges, depends on "node_section" currently in
    if node_section == 1:
        search_bounds = [0,edge_bounds[0]]
    elif node_section == 4:
        search_bounds = [edge_bounds[2], tot_edges]
    else:
        search_bounds = [edge_bounds[node_section-1], edge_bounds[node_section]]
        
    return search_bounds
    
    
def write_file(data_list, name, id):
    with open('./io/%s_%s.csv' %(name, id), 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        for data in data_list:
            writer.writerow(data)