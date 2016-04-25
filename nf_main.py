'''
Author: Adam Thomson            For: Network Flows
This program models a randomly generated Netflix delivery network, using Djikstra's Algorithm to find the shortest path
from a viewer to a NF data server and [Decide on Algorithm] to find the max flow through the network.  Every run, a set
of NF servers, ISP hubs of various sizes, and viewers will be randomly generated.  This network will be output as .csv
files similar to those provided so you can verify optimality.  It will then find the shortest path tree, max flow, and
min cut.  After finding these, I will model a network flood (new season of popular show) to model the impact on feasible
viewer demands.
'''


#import generate_network from nf_generate_network
#import shortest_paths from nf_sp
#import max_flow from nf_max_flow
#import min_cut from nf_min_cut
#import flood_network from nf_flood_network
#import calc_stats from nf_calc_status


if __name__ == '__main__':
    print '\nStarting NetflixDelivery.py...'
    print 'For usage explanation, see the README'
    print '\n\nGenerating network...'
    #generate_network()
    print '\n\nFinding shortest paths...'
    #shortest_paths()
    print '\n\nCalculating Max Flow and Min Cut...'
    #max_flow()
    #min_cut()
    print '\n\nFlooding Network...'
    #flood_network()
    print '\n\nCalculating Stats...'
    #calc_stats()