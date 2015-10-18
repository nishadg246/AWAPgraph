import networkx as nx
import random
from base_player import BasePlayer
from settings import *
import operator

class Player(BasePlayer):
    """
    You will implement this class for the competition. DO NOT change the class
    name or the base class.
    """

    # You can set up static state here
    has_built_station = False
    stations=[]
    taken=[]
    node_weights = []
    best_stations = []
    built_stations = []
    best_stations = []
    placed_stations =[]
    currStations=[]
    stations_to_build = []

    



    def __init__(self, state):
        """
        Initializes your Player. You can set up persistent state, do analysis
        on the input graph, engage in whatever pre-computation you need. This
        function must take less than Settings.INIT_TIMEOUT seconds.
        --- Parameters ---
        state : State
            The initial state of the game. See state.py for more information.
        """
        graph = state.get_graph()
        num_nodes = len(graph.nodes())

        if num_nodes < 100: n = 3
        elif num_nodes < 200: n = 4
        elif num_nodes < 400: n = 6
        elif num_nodes < 600: n = 9
        elif num_nodes < 1000: n = 15
        elif num_nodes < 1350: n = 17
        elif num_nodes < 1600: n = 20
        elif num_nodes < 1900: n = 23
        else: n = 25
        n-=1
 
        centrality = nx.degree_centrality(graph)
        sum_c = 0
        for i in xrange(num_nodes):
            sum_c += centrality[i]
        avg_c = sum_c / num_nodes
        self.node_weights = [0 for i in xrange(len(graph.nodes()))]

        for node in graph.nodes():
            if centrality[node] > avg_c:
                self.node_weights[node] += 4*centrality[node]
            for node_n in graph.neighbors(node):
                if centrality[node_n] > avg_c:
                    self.node_weights[node] += 2*centrality[node]
   
        for i in xrange(2*n):
            best = self.node_weights.index(max(self.node_weights))
            self.node_weights[best] = -1
            self.best_stations.append(best)

        NW = [0 for i in xrange(num_nodes)]
        for s in self.best_stations:
            sum_d = 0
            for t in self.best_stations:
                sum_d += len(nx.shortest_path(graph, s, t))
            NW[s] = sum_d

        for i in xrange(n):
            best = NW.index(max(NW))
            NW[best] = 0
            self.stations_to_build.append(best)
        print "tobiuld", self.stations_to_build
        
        self.best_stations = self.stations_to_build
        print self.best_stations

    # Checks if we can use a given path
    def path_is_valid(self, state, path):
        graph = state.get_graph()
        for i in range(0, len(path) - 1):
            if graph.edge[path[i]][path[i + 1]]['in_use']:
                return False
        return True

    def step(self, state):
        def noOverlap(a, b):
            lenA = len(a)
            lenB = len(b)
            edgeA = [(a[i],a[i+1]) for i in xrange(lenA-1)]
            edgeB = [(b[i],b[i+1]) for i in xrange(lenB-1)]
            return len(set(edgeA+edgeB)) == lenA - 1 + lenB - 1

        def noOverlapSet(a,s):
            for b in s:
                if not noOverlap(a, b):
                    return False
            return True

        def flatten(a):
            return [item for sublist in a for item in sublist]
        def path_to_edges(path):
            return [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

        def findBest(graph,pending_orders):
            if len(pending_orders) != 0:
                net=[]
                for order in pending_orders:
                    paths=[]
                    for stat in self.stations:
                        try:
                            a = nx.shortest_path(graph2, stat, order.get_node())
                            paths.append(a)
                        except:
                            paths=paths

                    for path in paths:
                        net.append((order,path,order.get_money()-(len(path)-1)*DECAY_FACTOR))
                if net==[]:
                    return None
                else:
                    maxnet=max(net,key=lambda x: x[2])
                    if maxnet[2]<=0:
                        return None
                    return maxnet



        """
        Determine actions based ofn the current state of the city. Called every
        time step. This function must take less than Settings.STEP_TIMEOUT
        seconds.
        --- Parameters ---
        state : State
            The state of the game. See state.py for more information.
        --- Returns ---
        commands : dict list
            Each command should be generated via self.send_command or
            self.build_command. The commands are evaluated in order.
        """

        # We have implemented a naive bot for you that builds a single station
        # and tries to find the shortest path from it to first pending order.
        # We recommend making it a bit smarter ;-)

        self.taken = [(a[0]-1,a[1])for a in self.taken if a[0]>1]
        commands=[]
        graph = state.get_graph()
        graph2 = graph.copy()


        if(len(self.taken)>0):
            graph2.remove_edges_from(flatten([path_to_edges(a[1]) for a in self.taken]))
        

        for x in xrange(1,len(self.best_stations)):
            if state.get_money() >= 1000*(1.5**x) and self.best_stations[x] not in self.stations:
                commands.append(self.build_command(self.best_stations[x]))
                self.stations.append(self.best_stations[x])

        #     if state.get_money() >= 1000*((1.5)**x) and self.best_stations[x] not in self.placed_stations:
        #         self.has_built_station=True
        #         commands.append(self.build_command(self.best_stations[x]))
        #         self.placed_stations.append(self.best_stations[x])
        #         print self.placed_stations

        if not self.has_built_station:
            commands.append(self.build_command(self.best_stations[0]))
            self.has_built_station = True
            self.stations.append(self.best_stations[0])

        # if state.get_money() >= 1500 and self.best_stations[1] not in self.stations:
        #     commands.append(self.build_command(self.best_stations[1]))
        #     self.stations.append(self.best_stations[1])


        # if state.get_money() >= 2250 and self.best_stations[2] not in self.stations:
        #     commands.append(self.build_command(self.best_stations[2]))
        #     self.stations.append(self.best_stations[2])



        # if state.get_money() >= int(2250*(1.5)) and station4 not in self.stations:
        #     commands.append(self.build_command(station4))
        #     self.stations.append(station4)

        # if state.get_money() >= int(2250*(1.5)*(1.5)) and station5 not in self.stations:
        #     commands.append(self.build_command(station5))
        #     self.stations.append(station5)

        # # if state.get_money() >= int(2250*(1.5)*(1.5)*(1.5)) and station6 not in self.stations:
        # #     commands.append(self.build_command(station6))
        # #     self.stations.append(station6)


        pending_orders = state.get_pending_orders()

        
        while True:
            best = findBest(graph2,pending_orders)
            if best==None:
                return commands
            else:
                pending_orders.remove(best[0])
                graph2.remove_edges_from(path_to_edges(best[1]))
                self.taken.append((len(best[1])-1,best[1]))
                commands.append(self.send_command(best[0],best[1]))

                # moves=[]
                # for element in net:
                #     if noOverlapSet(element[1],[s[1] for s in moves]) and self.path_is_valid(state,element[1]):
                #         moves.append(element)

                # for mov in moves:
                #     self.taken.append((len(mov[1])-1,mov[1]))
                #     commands.append(self.send_command(mov[0],mov[1]))
            
