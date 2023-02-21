import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain, combinations

class DsepGame:
    def __init__(self, num_nodes=5, k=1, debug=False):
        if num_nodes < 3 or num_nodes > 8:
            self.num_nodes = 5
        else:
            self.num_nodes = num_nodes  
        if k >= num_nodes - 3 or k<1:
            self.k = 1 
        else:
            self.k = k
        self.debug = debug
        self.score = 0
        self.lives = 3
        self.wins_in_level = 0
        self.newGame()
        

    
    def play(self, nodes_to_remove):
        if self.removed == False and self.adversary == False:
            for node_to_remove in nodes_to_remove:
                if node_to_remove in self.z1:
                    self.z1.remove(node_to_remove)
            DsepGame.plotGraphWithColors(self.D,self.x,self.y,self.z1)
            self.removed = True
            if not nx.algorithms.d_separated(self.D, set(self.x), set(self.y), set(self.z1)):
                self.lives = self.lives - 1
                print("You lost! The red nodes are still d-connected. You have ", self.lives, " more lives")
            else:
                print("Good job! Now the red nodes are d-separated. Let's see what the adversary chooses to add.")
                self.wins_in_level = self.wins_in_level + 1
                self.adversaryMove()
            if self.debug:
                print(self.x, "_|_", self.y, "|", self.z1, ":", nx.algorithms.d_separated(self.D, set(self.x), set(self.y), set(self.z1)))
                DsepGame.plotGraphWithUnblockedPaths(self.D,self.x,self.y,self.z1)
        elif self.removed == True and self.adversary == False:
            print("You already removed the nodes, call adversaryMove() to see what the adversary does.")
        else :
            print("You already removed the nodes and called the adversary, start a new level with newLevel()")      
    
    def adversaryMove(self):
        if self.removed == False and self.adversary == False:
            print("The first move is yours, choose a set of nodes to remove by calling removeNodes().")
        elif self.removed == True and self.adversary == False:          
            self.randomAdversary()
            print("The adversary chooses: ", self.nodes_to_add)
            DsepGame.plotGraphWithColors(self.D,self.x,self.y,self.z2)
            self.adversary = True
            if nx.algorithms.d_separated(self.D, set(self.x), set(self.y), set(self.z2)):
                self.score = self.score + self.num_nodes * self.k
                print("You won! The adversary could not d-connect the red nodes. Your new score is: ", self.score)
            else:
                self.score = self.score + 1
                print("It's a draw. The adversary d-connected the red nodes by adding at most k nodes. Your new score is: ", self.score)
            if self.debug:
                self.score = self.score + 1
                print(self.x, "_|_", self.y, "|", self.z2, ":", nx.algorithms.d_separated(self.D, set(self.x), set(self.y), set(self.z2)))
                DsepGame.plotGraphWithUnblockedPaths(self.D,self.x,self.y,self.z2)
        else:
            print("You already removed the nodes and called the adversary, start a new level with newLevel()")  
    
    def newGame(self):
        if self.lives > 0:
            if self.wins_in_level >= 3 and self.num_nodes  < 8:
                self.num_nodes = self.num_nodes + 1
                print("***** New level ***** : ", self.num_nodes, " nodes, k=", self.k)
                self.wins_in_level = 0
            if self.wins_in_level >= 3 and self.num_nodes  >= 8 and self.k < 3:
                self.num_nodes = 6
                self.k = self.k + 1
                print("***** New level ***** : ", self.num_nodes, " nodes, k=", self.k)
                self.wins_in_level = 0
                
            G = nx.complete_graph(self.num_nodes)
            self.G = nx.DiGraph([(u,v) for (u,v) in G.edges() if u<v])
            (self.D,self.x,self.y,self.z) = DsepGame.generateGraphAndStatement(self.num_nodes, self.k, self.G)
            print(".")
            print("*** New game: Can you make ", self.x[0], " and ", self.y[0], " d-separated by removing a node in ",self.z, "?")
            DsepGame.plotGraphWithColors(self.D,self.x,self.y,self.z)
            if self.debug:
                print(self.x, "_|_", self.y, "|", self.z, ":", nx.algorithms.d_separated(self.D, set(self.x), set(self.y), set(self.z)))
                DsepGame.plotGraphWithUnblockedPaths(self.D,self.x,self.y,self.z)
            self.z1 = self.z.copy()
            self.removed = False
            self.adversary = False
        else: 
            print("Game over, final score: ", self.score)


    def generateRandomDAG(num_nodes, prob_edge):
        # Generate random graph and make it become a DAG:
        G = nx.gnp_random_graph(num_nodes, prob_edge, directed = True)
        return nx.DiGraph([(u,v) for (u,v) in G.edges() if u<v])

    def plotGraphWithColors(D,x,y,z, edge_colors='black'):
        color_map = []
        for node in D:
            if node not in x and node not in y and node not in z:
                color_map.append('w')
            elif node not in z: 
                color_map.append('r')  
            else: 
                color_map.append('g')
        nx.draw_shell(D, node_color=color_map, with_labels=True, edgecolors = "black", edge_color=edge_colors)
        plt.show()

    def plotGraphWithUnblockedPaths(D,x,y,z):
        for path in nx.all_simple_paths(D.to_undirected(), source=x[0], target=y[0]):
            blocked = DsepGame.is_blocked(G=D, path=path,conditioned_nodes=z)
            if not blocked:
                edge_colors = []
                path_couples = []
                for i in range(len(path)-1):
                    src_node = path[i]
                    targ_node = path[i+1]
                    path_couples.append((src_node,targ_node))
                    path_couples.append((targ_node,src_node))
                for (u, v) in D.edges():
                    if (u,v) in path_couples:
                        edge_colors.append('r')
                    else:
                        edge_colors.append('black')
                DsepGame.plotGraphWithColors(D,x,y,z,edge_colors)
                plt.show()

    # This function is from the itertools page:
    def powerset(iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    ### The function below is a slight modification of the same function in dowhy.causal_graph.py (there is a lot of other things that are unnecessary for us, so I copy it here:
    def is_blocked(G, path, conditioned_nodes):
            """ Uses d-separation criteria to decide if conditioned_nodes block given path.
            """
            blocked_by_conditioning = False
            has_unconditioned_collider = False

            for i in range(len(path)-2):
                if G.has_edge(path[i], path[i+1]) and G.has_edge(path[i+2], path[i+1]): # collider
                    collider_descendants = nx.descendants(G, path[i+1])
                    if path[i+1] not in conditioned_nodes and all(cdesc not in conditioned_nodes for cdesc in collider_descendants):
                        has_unconditioned_collider=True
                        # print("Collider or its descendants are conditioned upon", path[i+1], collider_descendants, conditioned_nodes)
                else: # chain or fork
                    if path[i+1] in conditioned_nodes:
                        blocked_by_conditioning = True
                        break
            if blocked_by_conditioning:
                return True
            elif has_unconditioned_collider:
                return True
            else:
                return False

    def is_dsep_by_subset(D, x, y, z):
        dsep_subsets = []
        for cond in DsepGame.powerset(set(z)):
            c = []
            for c1 in cond:
                c.append(c1)
            if nx.algorithms.d_separated(D, set(x), set(y), set(c)):
                dsep_subsets.append(c)
        return dsep_subsets

    def is_dsep_by_removing_at_most_k_nodes (D, x, y, z, k=1):
        if nx.algorithms.d_separated(D, set(x), set(y), set(z)):
            return True
        else: 
            for dsep_subset in is_dsep_by_subset(D, x, y, z):
                if len(dsep_subset) >= len(z) - k:
                    return True
            return False

    def is_dsep_by_adding_nodes (D, x, y, z):
        if nx.algorithms.d_separated(D, set(x), set(y), set(z)):
            return z
        else: 
            other_nodes = []
            for n in D.nodes():
                if n != x[0] and n != y[0] and n not in z:
                    other_nodes.append(n)
            dsep_subsets = []
            for cond in DsepGame.powerset(other_nodes):
                c = []
                for z1 in z:
                    c.append(z1)
                for c1 in cond:
                    c.append(c1)
                if nx.algorithms.d_separated(D, set(x), set(y), set(c)):
                    dsep_subsets.append(c)
            return dsep_subsets

    def is_dsep_by_adding_at_most_k_nodes (D, x, y, z, k=1):
        if nx.algorithms.d_separated(D, set(x), set(y), set(z)):
            return True
        else: 
            for dsep_subset in is_dsep_by_adding_nodes(D, x, y, z):
                if len(dsep_subset) <= len(z) + k:
                    return True
            return False    

    def generateGraphAndStatement(num_nodes, k, G):    

        edges = G.edges()
        powerset_edges = [combinations(edges, r) for r in range(1,len(edges))]

        edges_to_be_removed = []
        for i in powerset_edges:
            for j in i:
                edges_to_be_removed.append(j)

        np.random.shuffle(edges_to_be_removed)
        
        print("Generating the correct problem", end='')
            
        for i in edges_to_be_removed:
            D = G.copy()
            print(".", end='')
            for (u,v) in i:
                if (u,v) in D.edges():
                    D.remove_edge(u,v) 
                    for x1 in D.nodes():
                        for y1 in D.nodes():
                            if x1==y1: 
                                continue
                            desc = nx.descendants(D.to_undirected(), source=x1)
                            if y1 not in desc:
                                continue
                            possible_nodes = list(D.nodes())
                            possible_nodes.remove(x1)
                            possible_nodes.remove(y1)
                            x = [x1]
                            y = [y1]

                            all_dseps = DsepGame.is_dsep_by_adding_nodes (D, x, y, [])

                            for dsep in all_dseps:
                                # If it can be d-separated (which means there is a solution to the initial state): 
                                other_nodes = []
                                for n in D.nodes():
                                    if n != x1 and n != y1 and n not in dsep and n not in other_nodes:
                                        other_nodes.append(n)
                                
                                potential_initial_states = []
                                ###for k1 in range(k, 0, -1):
                                if 1:
                                    k1 = k
                                    for z in combinations(other_nodes, k1):
                                        c = []
                                        for ds in dsep:
                                            c.append(ds)
                                        for z1 in z:
                                            c.append(z1)
            
                                        # If it is dconnected adding two sets of k nodes to the initial state):
                                        if c not in all_dseps and not nx.algorithms.d_separated(D, set(x), set(y), set(c)):
                                            if c not in potential_initial_states:
                                                potential_initial_states.append(c)
                                if len(potential_initial_states) >= 2:
                                    return (D,x,y,c)
                                            #print(x,y,dsep,c, nx.algorithms.d_separated(D, set(x), set(y), set(c)))
                                            #other_nodes2 = []
                                            #for n in D.nodes():
                                            #    if n != x1 and n != y1 and n not in c:
                                            #        other_nodes2.append(n)
                                            # If it is dconnected adding k different nodes to the initial state:
                                            #for k2 in range(1,k+1):
                                            #    for adv_z in combinations(other_nodes2, k2):
                                              #      c2 = dsep.copy()
                                              #      for adv_z1 in adv_z:
                                              #          c2.append(adv_z1)
                                               #     #print(x,y,c2, nx.algorithms.d_separated(D, set(x), set(y), set(c2)))
                                               #     if c2 not in all_dseps:
                                               #         return (D,x,y,c)
        if k > 1:
            (D,x,y,c) = generateGraphAndStatement(num_nodes, k-1, G)
            return (D,x,y,c)
        
        return (None, None, None, None)

    def randomAdversary(self):
        possible_choice = [n for n in self.D.nodes() if n != self.x[0] and n!= self.y[0] and n not in self.z]
        k1 = min(self.k, len(possible_choice))
        nodes_to_add = np.random.choice(possible_choice, k1, replace = False)
        z2 = self.z1.copy()
        for node_to_add in nodes_to_add:
            if node_to_add not in z2:
                z2.append(node_to_add)
        self.z2 = z2
        self.nodes_to_add = nodes_to_add
   