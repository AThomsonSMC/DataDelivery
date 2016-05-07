'''
Author: Adam Thomson            For: Network Flows
This program models a randomly generated data delivery network, using Topological Sort to find the shortest path
from a data server to users and [Decide on Algorithm] to find the max flow through the network.  Every run, a set
of data servers, ISP hubs and nodes, and users will be randomly generated.  This network will be output as .csv
files similar to those provided so you can verify optimality.  It will then find the shortest path tree, max flow, and
min cut.
'''


from nf_generate_network import generate_network
from nf_sp import topological_sort
#import max_flow from nf_max_flow
#import min_cut from nf_min_cut
#import flood_network from nf_flood_network
#import calc_stats from nf_calc_status

from time import time                           #Gives number of seconds since epoch

if __name__ == '__main__':
    TIMESTAMP = int(time()*1000)
    ID = TIMESTAMP % 10000          #Unlikely to run program exactly n*10 seconds apart with millisecod accuracy
    print '\nStarting Network Flows DataDelivery.py...'
    print 'For usage explanation, see the README'
    nodes, edges, node_boundaries, edge_boundaries = generate_network(ID)
    print '\nFinding shortest paths...'
    topological_sort(nodes, edges, node_boundaries, edge_boundaries, ID)
    print '\nCalculating Max Flow and Min Cut...'
    #max_flow()
    #min_cut()
    print '\n\nFlooding Network...'
    #flood_network()
    print '\n\nCalculating Stats...'
    #calc_stats()