'''
Adam Thomson            Network Flows
This program models a randomly generated data delivery network.  Every run, a set of data servers, ISP hubs and nodes,
and users will be randomly generated.  This network will be output as .csv files similar to those provided in the sample
project so you can verify optimality.  It will then find the shortest path tree, max flow, and min cut.  I've added the
constraint that every user must receive at least 1 unit of flow.  From my testing, I can not find a difference in the
max flow/min-cut.  Of course, this has an impact on the total cost of the network, but a user with no delivery is not a user!
'''

from nf_generate_network import generate_network
from nf_sp import topological_sort
from nf_max_flow import max_flow
from nf_min_cut import min_cut

from time import time                           #Gives number of seconds since epoch

if __name__ == '__main__':
    TIMESTAMP = int(time()*1000)
    ID = TIMESTAMP % 10000          # Unlikely to run program exactly n*10 seconds apart with millisecod precision
    print '\nStarting Network Flows DataDelivery.py...'
    nodes, edges, node_bounds, edge_bounds = generate_network(ID)
    print '\nFinding shortest paths...'
    topological_sort(nodes, edges, node_bounds, edge_bounds, ID)
    print '\nCalculating Max Flow...'
    max_flow(nodes, edges, node_bounds, edge_bounds, ID)
    print '\nFinding Min-Cut...'
    min_cut(nodes, edges, node_bounds, edge_bounds, ID)
    print '\n\nProgram is finished.  Files are in the /io/ folder.'