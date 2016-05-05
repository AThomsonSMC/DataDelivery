'''
Find the max-flow through the system - Use [Algorithm] to find the state that maximizes global flow while
satisfying demands.  By starting with a feasible network and then optimizing, we reduce runtime over starting with nothing
and incrementally pushing units of flow.
'''

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
    

def check_demand(node, node_bounds):
    demand = node[1]
    if demand == 0: return True
    
    


def max_flow(nodes, edges, node_bounds, edge_bounds, timestamp):
    pass