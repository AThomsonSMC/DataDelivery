'''
Find the shortest path to each node.  Using Djikstra's algorithm.
'''

#TODO: Read graph data from generate_network
#Using provided test data
nodes = [               #[node_id, demand]
  [0, 4],
  [1, 5],
  [2, 0],
  [3, 0],
  [4, 0],
  [5, 0],
  [6, -3],
  [7, -6]
]

edges = [               #[edge_id, tail_id, head_id, capacity, cost]
  [0, 0, 1, 3, 10],
  [1, 0, 3, 1, 10],
  [2, 3, 0, 2, 10],
  [3, 1, 2, 1, 10],
  [4, 2, 3, 3, 10],
  [5, 2, 5, 3, 10],
  [6, 4, 2, 2, 10],
  [7, 3, 5, 1, 10],
  [8, 5, 3, 3, 10],
  [9, 5, 4, 2, 10],
 [10, 4, 5, 1, 10],
 [11, 4, 6, 3, 10],
 [12, 6, 4, 3, 10],
 [13, 5, 6, 2, 10],
 [14, 5, 7, 3, 10],
 [15, 6, 7, 2, 10],
 [16, 7, 6, 2, 10]
]

def djikstras_algorithm(nodes, edges):
    visited_nodes = []

    output = {}
    for node in nodes:
        output[node[0]] = [9999, 9999]

    #start at node 0
    cur_node = 0
    output[0] = [0,0]

    while len(visited_nodes) < len(nodes):
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
        cur_label = 999

        #find the node with the lowest label and continue algorithm
        for node in output:
            if node not in visited_nodes and output[node][1] < cur_label:
                cur_node = node
                cur_label = output[node][1]

    print output

    print "Shortest paths have been found"


if __name__ == '__main__':
    djikstras_algorithm(nodes, edges)