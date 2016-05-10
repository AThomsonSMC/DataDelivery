'''
Find the max-flow through the system - Use a preflow push algorithm to find the state that maximizes global flow while
satisfying demands.  By starting with an optimal network and then making feasible, we reduce runtime over starting with nothing
and incrementally pushing units of flow.
'''

import nf_utils

def get_cap_flow_matrix(nodes, node_bounds, edges, edge_bounds):
    n = len(nodes)
    cap_m = [[0]*n for i in range(0,n)]       #Initialize to 0 nxn matrix
    flow_m = [[0]*n for i in range(0,n)]      #Initialize to 0 flow in network
    for node in nodes:
        ob_edges = nf_utils.find_ob_edges(node[0], node_bounds, edges, edge_bounds)
        for edge in ob_edges:
            cap_m[edge[1]][edge[2]] = edge[3]
            
    return cap_m, flow_m

def max_flow(nodes, edges, node_bounds, edge_bounds, timestamp):
    
    #Define variables used throughout algorithm
    n = len(nodes)
    height = [0] * n       # initialize all nodes to 0 height
    ex = [0] * n            # all nodes have 0 excess to start
    seen = [0] * n     # keep track of nodes that have been seen by each node
    
    #Add all nodes except source and sink to list of active nodes
    active_nodes = []
    for node in nodes:
        if node != nodes[0] and node != nodes[-1]:
            active_nodes.append(node[0])
    
    #Create the capacity and flow matrices.
    cap_matrix, flow_matrix = get_cap_flow_matrix(nodes, node_bounds, edges, edge_bounds)
    
    # Next, define the subroutines
    def push(i, j):         # Perform a flow push on edge
        flow = min(ex[i], cap_matrix[i][j] - flow_matrix[i][j])
        flow_matrix[i][j] += flow
        flow_matrix[j][i] -= flow
        ex[i] -= flow
        ex[j] += flow
        if j > i:
            edge = nf_utils.get_ij_edge(i, j, edges)
            edge[5] += flow
        else:
            edge = nf_utils.get_ij_edge(j, i, edges)
            edge[5] -= flow
    
    def relabel(i):      # Find smallest height that allows for push
        min_height = nf_utils.INFINITY
        for j in range(0,n):
            if cap_matrix[i][j] - flow_matrix[i][j] > 0:
                min_height = min(min_height, height[j])
                height[i] = min_height + 1
                
    def rid_excess(i):
        while ex[i] > 0:
            if seen[i] < n:
                j = seen[i]    # Checking potential edge [i,j]
                if cap_matrix[i][j] - flow_matrix[i][j] > 0 and height[i] > height[j]:
                    push(i, j)
                else:
                    seen[i] += 1   # No valid neighbors
            else:
                relabel(i)      #All valid neighbors checked, still have excess, raise i's height
                seen[i] = 0
    
    print 'Initializing preflow...'
    height[0] = n
    ex[0] = nf_utils.INFINITY
    
    # Push flow from source.  We know only [node_bounds[0]:node_bounds[1]] are neighbors of source
    for node in range(1,node_bounds[1]):
        push(0, node)
        ex[0] = nf_utils.INFINITY       #Reset excess on source to infinity so it will get pushed to next DC
    
    # Each user must recieve at least 1 unit of flow.  Set some ISP->User edges to 1 unit of flow
    for edge in edges[edge_bounds[2]:edge_bounds[3]]:
        i, j = edge[1], edge[2]
        if ex[j] == 0:       #If user already has flow, no need to provide more for now
            flow_matrix[i][j] = 1
            edge[5] += 1
            ex[i] -= 1
            ex[j] += 1
    
    print 'Every user has at least one unit of flow...'
    cur = 0
    while cur < len(active_nodes):
        i = active_nodes[cur]
        orig_height = height[i]
        rid_excess(i)
        #If height[i] is now higher, move i to front of active_nodes and retry with new height
        if height[i] > orig_height:
            active_nodes.insert(0, active_nodes.pop(cur))
        else:
            # Node got rid of excess without needing to raise height, go to next node in active_nodes list
            cur += 1
            
    max_flow = 0
    for flow in flow_matrix[0]:
        max_flow += flow
         
    print 'Found max flow!  It is %s' %max_flow  
    
    # Now write the results to max_flow.csv
    flow_output = []
    edge_output = []
    for edge in edges:
        flow_output.append([edge[0],edge[5]])
        edge_output.append(edge[:5])
    print "Writing maximum flow to max_flow_%s.csv" %timestamp 
    nf_utils.write_file(flow_output,'max_flow',timestamp)
    print "Writing edge data to edges_%s.csv" %timestamp
    nf_utils.write_file(edge_output,'edges',timestamp)

#
#  !! This is an experimental algorithm that I tried to implement but couldn't convince myself that I could formally prove its correctness.
#  !!  Instead, I implemented the standard preflow-push algorithm above for the sake of completing the project.
#  !! I plan on revisiting this to see if I can get better performance by the nature of the topology of the graph.  What I'd like to show
#  !!  is that I can get complexity of O(m*(n_1^2+n_2^2+n_3^2+n_4^2)) < O(m*n^2) for some sets of n's, minimizing at n_i = .25*n for O((n^2/16)*m)
#  !! It does not run as-is, but I wanted to include the algorithm sketch to show what I was thinking
#
'''        
        
def mincost_experiment(nodes, edges, node_bounds, edge_bounds, timestamp):
    #
    #  Use a modified preflow-push algorithm to find the min-cost flow.  Initialize the flow graph by pushing flow = min(demand, capacity)
    #  on ISP->User nodes.  Then calculate the total flow out of ISP nodes, and push flows from HUBs to satisfy (using lowest cost edges),
    #  and repeat from DCs to HUBs.  Once this preflow is found, iterate over user nodes to find excess flow (will never have shortage,
    #  generate_network checks for capacity feasibility before writing output).  Remove flow from highest cost edges until flow = demand.
    #                                                                             ^By highest cost, I'm using (edge_head_distance + cost)
    #  Once user demands are satisfied, repeat this process on ISPs and HUBs.  This will produce the min-cost flow that satisfies user demands.
    tot_flow = {}
    for edge in edges:
        flow[edge[0]] = 0
        
    for node in nodes[node_bounds[3]:]:
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                edge[5] += node[1]          #increment flow on edge by node demand
                if edge[5] > edge[3]: edge[5] = edge[3]     #if flow > cap, flow = cap

    # ISP->User edges all have flow, calc total flow through each ISP and send that flow through each incoming edge
    for node in nodes[node_bounds[2]:node_bounds[3]]:
        for edge in edges[edge_bounds[2]:]:
            if edge[1] == node[0]:
                node[1] += edge[5]          #increment "demand" on ISP node.  Will be set back to 0 once pushing that flow on inbound edges
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0                         #reset demand on ISP node to 0, it is transitionary
                
    #Repeat on HUBs
    for node in nodes[node_bounds[1]:node_bounds[2]]:
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[1] == node[0]:
                node[1] += edge[5]
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0
       
    #Finally repeat on DCs
    for node in nodes[node_bounds[0]:node_bounds[1]]:
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[1] == node[0]:
                node[1] += edge[5]
        for edge in edges[:edge_bounds[0]]:
            if edge[2] == node[0]:
                edge[5] += node[1]
                if edge[5] > edge[3]: edge[5] = edge[3]
        node[1] = 0                 #DCs hace 0 demand, total demand is aggregated at source node
       
       
    # Network is now flooded, reduce flow into user nodes until demand is just satisfied, removing flow from most costly edges first
    for node in nodes[node_bounds[3]:]:
        ib_edges = []
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)   #Sort the inbound edges by their cost and then reverse for desc
        excess = get_node_excess(node, ib_edges, [])
        while excess > 0:
            ib_edges[0][5] = 0                              #Set most expensive inbound edge flow to 0
            excess = get_node_excess(node, ib_edges, [])    #Get node's new excess
            if excess < 0:
                ib_edges[0][5] += -1*excess                 #If removed too much flow, readd some to meet demand
            else:
                ib_edges.pop(0)                             #Remove edge from list of inbound edges
                
    # Users now have satisfied demands and no excess, remove excess on HUB->ISPs
    for node in nodes[node_bounds[2]:node_bounds[3]]:
        ib_edges = []
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[2]:]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    # Repeat for DC->HUB edges
    for node in nodes[node_bounds[1]:node_bounds[2]]:
        ib_edges = []
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[1]:edge_bounds[2]]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    # Finally, repeat on source->DC edges
    for node in nodes[node_bounds[0]:node_bounds[1]]:
        ib_edges = []
        for edge in edges[:edge_bounds[0]]:
            if edge[2] == node[0]:
                ib_edges.append(edge)
        ob_edges = []
        for edge in edges[edge_bounds[0]:edge_bounds[1]]:
            if edge[2] == node[0]:
                ob_edges.append(edge)
        ib_edges.sort(key=lambda x: x[4], reverse=True)
        excess = get_node_excess(node, ib_edges, ob_edges)
        while excess > 0:
            ib_edges[0][5] = 0
            excess = get_node_excess(node, ib_edges, [])
            if excess < 0:
                ib_edges[0][5] += -1*excess
            else:
                ib_edges.pop(0)
                
    print 'Min-cost flow found!'
'''