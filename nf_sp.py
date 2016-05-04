'''
Find the shortest path to each node.  Using Djikstra's algorithm.
'''

import csv

#This is test data for a small, acyclic graph
test_nodes = [               #[node_id, demand]
  [0, 4],
  [1, 5],
  [2, 0],
  [3, 0],
  [4, 0],
  [5, 0],
  [6, -3],
  [7, -6]
]

test_edges = [               #[edge_id, tail_id, head_id, capacity, cost]
  [0, 0, 1, 99, 2],
  [1, 0, 4, 99, 4],
  [2, 1, 2, 99, 1],
  [3, 1, 5, 99, 5],
  [4, 4, 5, 99, 3],
  [5, 5, 2, 99, 1],
  [6, 5, 6, 99, 5],
  [7, 2, 6, 99, 4],
  [8, 6, 3, 99, 3],
  [9, 6, 7, 99, 6],
 [10, 3, 7, 99, 1]
]

def write_sp(output, timestamp):
    with open('sp_%s.csv' %timestamp, 'wb') as spfile:
        spwriter = csv.writer(spfile, delimiter=',')
        for node in output:
            spwriter.writerow([node, output[node]])

def djikstras_algorithm(nodes, edges, timestamp):
    visited_nodes = []

    output = {}
    for node in nodes:
        #print node
        output[node[0]] = [999999999999, 999999999999]

    #start at node 0
    cur_node = 0
    output[0] = [0,0]

    while len(visited_nodes) < len(nodes):
        if len(visited_nodes) % 100 == 0:
            print 'Labeled %s nodes' %len(visited_nodes)
        hit_nodes = []
        hit_edges = []
        for edge in edges:
            if edge[1] == cur_node and edge[2] not in visited_nodes:
                hit_nodes.append(edge[2])
                hit_edges.append(edge[0])
        for i in range(len(hit_nodes)):
            #if current cost is greater than current distance + edge cost, update cost and parent node
            if output[hit_nodes[i]][1] > output[cur_node][1] + edges[hit_edges[i]][4]:
                output[hit_nodes[i]] = [cur_node, output[cur_node][1] + edges[hit_edges[i]][4]]
        visited_nodes.append(cur_node)
        
        cur_label = 9999
        #find the node with the lowest label and continue algorithm
        for node in output:
            if node not in visited_nodes and output[node][1] < cur_label:
                cur_node = node
                cur_label = output[node][1]

    print "Shortest paths have been found"
    write_sp(output, timestamp)
    
    
def topological_sort(nodes, edges, timestamp):
    pass
    node_distances = {}
    queued_nodes = []
    done_nodes = []
    output = {}
    
    for node in nodes:
        node_distances[node[0]] = 99999     #Initialize every node to effectively infinity distance
        output[node[0]] = -1                #Initialize every node's parent to invalid -1
    
    cur_node = nodes[0][0]          #the id of the currently inspected node
    node_distances[cur_node] = 0    #source node is 0 distance from itself
    output[cur_node] = cur_node     #source node's parent is itself
    
    while len(done_nodes) < len(nodes):
        for edge in edges:
            if edge[1] == cur_node:
                if edge[2] not in queued_nodes and edge[2] not in done_nodes:
                    queued_nodes.append(edge[2])
                if node_distances[edge[2]] > (node_distances[cur_node] + edge[4]):
                    node_distances[edge[2]] = node_distances[cur_node] + edge[4]
                    output[edge[2]] = edge[1]
        done_nodes.append(cur_node)
        
        try:
            cur_node = queued_nodes.pop(0)      #Set cur_node to first element of queue and remove
        except IndexError:
            cur_node = -1               #Queue is empty, set cur_node to invalid id
        
        
    if len(queued_nodes) > 0:
        print 'Something went wrong, there are still queued nodes!!'
        
    write_sp(output, timestamp)
        
        
if __name__ == "__main__":
    topological_sort(test_nodes, test_edges, 'TEST123')