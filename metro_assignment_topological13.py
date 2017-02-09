# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:23:30 2016



"""
# importer la liste
import os

os.chdir(r'C:\Users\Godzila\Desktop\DSTI\Algorithms')

results = []
with open('metro_complet.txt') as inputfile:
    for line in inputfile:
        results.append(line.strip().split(' '))
        
'''
First exercise: create a path between two stations
Step 1: Create the adjacent list {station:[station1,station2,...,station n]}
    A. In the file, separate Stations names and weighted routes 
            --> prepare(mylist), return a list of weighted routes
    B: Create the adjacent list
        --> dic(mylist), return the adjacent list {station:[station1,station2,...,station n]}

'''
       
#OK to compute the complexity and the run time      
#séparer les deux listes (noms des stations et trajets)
def prepare(mylist):
    lS_liste_station=[]#accueille le numéro et nom des stations
    lS_routes=[]#accueille des doublets[source-destination]
    
    for row in mylist:#la séparation se fera sur le nombre de caractères codés en première colonne
        S_first_item=row[0]
        
        if len(S_first_item)==4:#les stations sont codées avec 4caractères (ajouts de zéros)
            lS_liste_station.append(row)
        elif len(S_first_item)<4:#les stations sont codées avec au maximum trois caractères pour les trajets
            lS_routes.append(row)
    
    return lS_routes#retourne la liste des doublets [source-destination]
    
#OK to compute the complexity and the run time   
#créer linked list:dictionnaire trajets: keys are source (départ), values are destinations
#{station:[neighbour1,neighbour2,neighbour3...]}
def dic(mylist):
    LS_dic_trajets={}#initialize dictionary
    LS_trajets=prepare(mylist)#fill the list of trajets [source - destination]
    for row in LS_trajets:#for each doublet
        S_source=row[0]
        S_destination=row[1]
        if S_source not in LS_dic_trajets.keys(): #if the source is not already in the dictionary
            LS_new_neighbour=[]#initialize a list for the linked stations(destinations)
            LS_new_neighbour.append(S_destination)#append the current destination
            LS_dic_trajets[S_source]=LS_new_neighbour#append it to the source in the dictionary
        else:
            LS_dic_trajets[S_source].append(S_destination)#if the source already in the dictionary, append to the asscoiate destinations the current one
    return LS_dic_trajets


'''Step2: find the path between two stations
        A. Create a BFS
           --> BFSmetro(mylist,departure), return the list of visited stations from a departure station 
        B: Use this BFS to compute a path between two nodes:
            --> findpath2(mylist,departure,destination): return a list of stations (path between two stations)
        C: Replace each station number by its name
            --> prepare_station(mylist): to bind each station number with it's name - return a list [station_number, name]
            --> path_with_name(mylist,departure,arrival): return a list of stations (names) between two stations
'''
#test=BFSmetro(results,'1')
#visit all metro station using BFS. Must visit once every station
#test_ok:len(test)=376  

#cost: O(n)
def BFSmetro(mylist,departure):
    dict_linkedlist=dic(mylist)#import linkedlist stations
    lS_visited=[departure]#define a list of visited stations
    lS_queue=[departure]#define a queue of stations to visit(we know that they are linked to visited stations)

    while lS_queue!=[]:#to do until the queue is empty
        for station in lS_queue:#for each station in the queue  O(n)
            sL_children=dict_linkedlist[station]#sL_children are stations related to the station visited
            for value in sL_children:#for each linked station  O(6) because my max nb of child per staion=6
                if value not in lS_visited:#if the station has not yet been visited
                    lS_queue.append(value)#increment the queue with this station
                    lS_visited.append(value)#add this station to the visited station
            lS_queue=lS_queue[1:]#pop the first value of the queue

    return lS_visited#return all the visited stations
    
#test=DFSmetro(results,'92')
def DFSmetro(mylist,start_station):
    dict_linkedlist=dic(mylist)
    visited=[]
    stack=[]
    visited=[start_station]
    for station in dict_linkedlist[start_station]:
        stack.append(station)
    while stack!=[]:
        #print('step1'+str(stack))
        current_search=stack.pop()
        if current_search not in visited:
            visited.append(current_search)
            #print('step1bis'+str(visited))
            if current_search in dict_linkedlist.keys():
                #print('step2 node_key'+str(current_search))
                values=dict_linkedlist[current_search]
                #print('step2bis_values_tree'+str(values))
                for value in values:
                    #print('step3_value'+str(value))
                    stack.append(value)
                    #print('step4_stack'+str(stack))

    return visited

#OK to compute the complexity and the run time      
#test=find_path2(results,'1','17') -len=49
#find a path between two stations using BFS
def find_path2(mylist,departure,destination):
    lS_mypath=BFSmetro(mylist,departure)#initialize the path with the station visited using BFS from the departure station
    s_end=lS_mypath.index(destination)+1#find the index of the arrival station in lS_mypath
    lS_mypath=lS_mypath[:s_end]#cut lS_mypath after the arrival station
    return lS_mypath
    
#OK to compute the complexity and the run time  
#Map station number with stations name
#test=prepare_station(results)
#len(test)=376 ok
def prepare_station(mylist):
    row=0
    ls_liste_station=[]
    
    for row in mylist:
        first_item=row[0]
        
        if len(first_item)==4:
            ls_liste_station.append(row)
    
    ls_liste_sans_espaces=[]
    i=0
    
    for line in ls_liste_station:#concatène les noms spéarés dans liste_station
        S_nom_station=''
        for i in range(1,len(line)):
            S_nom_station+=line[i]
        ls_liste_sans_espaces.append(S_nom_station)#retourne la luste des noms de stations
    
    ls_liste_station_clean=[]
    count=0
    for line in ls_liste_station:#fait matcher les numeros de station avec leurs noms
        temp_station=[]
        temp_station.append(line[0])
        temp_station.append(ls_liste_sans_espaces[count])
        ls_liste_station_clean.append(temp_station)
        count+=1
            
    return ls_liste_station_clean

#OK to compute the complexity and the run time      
#test=path_with_names(results,'1','17') -len(test)=49 same as find_path2,Ok
#reprend le path de find_path, et remplace les numeros de station par leur nom
def path_with_names(mylist, departure, arrival):
    LS_path=find_path2(mylist, departure, arrival)#initialize path using find_path2
    LS_path_with_name=[]#create emplty list for path with name in letters
    ls_liste_stations=prepare_station(mylist)#take the liste of [n°station - name station]created before
    for station in LS_path:#for each staton in the path with station numbers
        for value in ls_liste_stations:#in the liste [n°station-station]
            s_nb_station=value[0]#take the first value n°station
            #i=0
            for i in s_nb_station:
                count=1
                if i=='0':#remove initial zeros to match the format in the path
                    s_nb_station=s_nb_station[count:len(s_nb_station)]
            if s_nb_station==station:#if we find a correspondance in the n°station in the two lists:
                LS_path_with_name.append(value[1])#add to the path_with_names the name in letters
    return LS_path_with_name
    
'''
Second exercice: create a topological sort
    Step1: Create a dictionary of levels
            --> dic_in_degrees_stations(mylist): create a linked list of {station:{[incoming station1, incoming station 2 etc...]}
            --> dic_in_degrees_degrees(mylist): create a linkedlist {station:nb in_degrees}, counting the number of stations linked to one station in dic_in_degrees_stations
            --> dic_layers(mylist): return a linked list {nb_in_degrees:[station1,station2...]}
    Step2: create a topological sort based on dfs. 
    Step3: find critical path
            '''
    
#OK to compute the complexity and the run time    
#test=dic_layers(results)   #create a linkedlist{nb_in_degrees:[station1,station2...]}  
#len(test[1])+len(test[2])+len(test[3])+len(test[4])+len(test[5])+len(test[6]) =376 #Ok 
def nb_layers(mylist):
    d_dic_in_degrees=in_degrees(mylist)
    sL_degrees_values=d_dic_in_degrees.values()
    nb_layers=max(sL_degrees_values)#My maximum number of in_degrees is my number of layers
    #print('nb layers='+str(nb_layers))
    d_dic_layers={}
    for station in d_dic_in_degrees:
        lS_temp_values=d_dic_in_degrees[station]
        if lS_temp_values not in d_dic_layers:
            d_dic_layers[lS_temp_values]=[station]
        else:
            d_dic_layers[lS_temp_values].append(station)
    return nb_layers 
    
def parents(mylist):
    dict_linkedlist=dic(mylist)
    dict_parents={}
    for station in dict_linkedlist.keys():
        lS_child=dict_linkedlist[station]
        for child in lS_child:
            if child not in dict_parents.keys():
                dict_parents[child]=[station]
            else:
                dict_parents[child].append(station)
    return dict_parents
        

def in_degrees(mylist):
    dict_linkedlist=dic(mylist)
    dict_in_degrees={}
    lS_values=[]

#obtain all values (so have at least 1 in degree)

    for values in dict_linkedlist.values(): 
        for value in values:
            lS_values.append(value)

#Initialize dict_in_degrees
    for value in lS_values:
        if value not in dict_in_degrees:
            dict_in_degrees[value]=0

    for value in dict_in_degrees.keys():
        for key in dict_linkedlist.keys():
            if value in dict_linkedlist[key]:
                dict_in_degrees[value]+=1

    return(dict_in_degrees) 
    
#test_topo=topological(results,'92')
#len(test_topo)=376: Ok!
def topological(mylist,start_station):
    dict_linkedlist=dic(mylist)
    dict_parents=parents(mylist)
    dict_in_degrees=in_degrees(mylist)
    stack=[]
    lS_topo=[start_station]
    lS_all_visited=[start_station]
    for nodes in dict_linkedlist[start_station]:
        stack.append(nodes)
    while stack!=[]:
        #print('stack '+str(stack))
        current_search=stack.pop()
        if current_search not in lS_topo:
            lS_all_visited.append(current_search)
            lS_topo.append(current_search)
            #print('dict_in_degrees '+str(current_search)+' = '+str(dict_in_degrees[current_search]))
            del dict_in_degrees[current_search]
            #print('visited'+str(visited))
            if current_search in dict_linkedlist.keys():
                #print('current_search '+str(current_search))
                values=dict_linkedlist[current_search]
                #print('children '+str(values))
                for value in values:
                    #print('child '+str(value))
                    if value not in lS_topo:
                        lS_all_visited.append(value)
                        dict_in_degrees[value]-=1
                        min_layer=min(dict_in_degrees.values())
                        if dict_in_degrees[value]==min_layer:
                            stack.append(value)
                            #print('new stack '+str(stack))
                        else:
                            for parent in dict_parents[value]:
                                stack.append(parent)
                    else:
                        lS_all_visited.append(current_search)
        else:
            lS_all_visited.append(current_search)

    return lS_topo
    
    
def nb_layers(mylist):
    d_dic_in_degrees=in_degrees(mylist)
    sL_degrees_values=d_dic_in_degrees.values()
    nb_layers=max(sL_degrees_values)#My maximum number of in_degrees is my number of layers
    #print('nb layers='+str(nb_layers))
    d_dic_layers={}
    for station in d_dic_in_degrees:
        lS_temp_values=d_dic_in_degrees[station]
        if lS_temp_values not in d_dic_layers:
            d_dic_layers[lS_temp_values]=[station]
        else:
            d_dic_layers[lS_temp_values].append(station)
    return nb_layers 

    
#test=critical_path(results,'1','176')#doesn't work
def critical_path(mylist,start_station, end_station):
    dict_linkedlist=dic(mylist)
    dict_parents=parents(mylist)
    dict_in_degrees=in_degrees(mylist)
    stack=[]
    lS_topo=[start_station]
    lS_all_visited=[start_station]
    for nodes in dict_linkedlist[start_station]:
        stack.append(nodes)
    while stack!=[]:
        #print('stack '+str(stack))
        current_search=stack.pop()
        if current_search not in lS_topo:
            lS_all_visited.append(current_search)
            lS_topo.append(current_search)
            #print('dict_in_degrees '+str(current_search)+' = '+str(dict_in_degrees[current_search]))
            del dict_in_degrees[current_search]
            #print('visited'+str(visited))
            if current_search in dict_linkedlist.keys():
                #print('current_search '+str(current_search))
                values=dict_linkedlist[current_search]
                #print('children '+str(values))
                for value in values:
                    #print('child '+str(value))
                    if value not in lS_topo:
                        lS_all_visited.append(value)
                        dict_in_degrees[value]-=1
                        min_layer=min(dict_in_degrees.values())
                        if dict_in_degrees[value]==min_layer:
                            stack.append(value)
                            #print('new stack '+str(stack))
                        else:
                            for parent in dict_parents[value]:
                                stack.append(parent)
                    else:
                        lS_all_visited.append(current_search)
        else:
            lS_all_visited.append(current_search)
            
    

    return lS_all_visited
    

'''Third exercise: implement a Djikstra algorithm using Fibonacci heap
    Step 1: create a dictionary of weighted nodes
        Fibonacci heap uses weighted nodes. We don't have weights for nodes, only for edges, so
        we "transform" the edges in nodes. ex:[1,12] becomes '[1,12]'
        -->dic_weight_edges(mylist): return a dictionary {'[station1,station2]':weight}
    Step 2: create an adjacent list of parents and an adjacent list of children
            Fibonacci heap use pointers to parents and childs, so we need to create linked list too obtain these pointers
        --> dic_parents(mylist): return a linked list {'[station1,station2]':'[station0,station1]','[station22,station1]' etc...}
        --> dic_child(mylist): return a linked list {'[station1,station2]':'[station2,station3]','[station2,station365] etc...}
    Step 3: create the in_degrees list for each weighted edge
            Fibonacci heap uses in_degrees
    
'''



#test=dic_weighted_edges(results)  {'[station1,station2]':weight}
#len(test)=933:Ok
def dic_weighted_edges(mylist):
    sL_weighted_routes=prepare(mylist)
    dict_weighted_edges={}
    for line in sL_weighted_routes:
        sL_edge=str([line[0],line[1]])
        int_weight=line[2]
        if int_weight=='120.0':
            int_weight='120'
        int_weight=int(int_weight)
        #if sL_edge not in dict_weighted_edges.keys():
        dict_weighted_edges[sL_edge]=int_weight
        #else:
        #dict_weighted_edges[sL_edge].append(int_weight)
    return dict_weighted_edges

#test=dic_child_edges(results)    
def dic_child_edges(mylist):
    dict_linkedlist=dic(mylist)
    dict_child_edges={}
    for station in dict_linkedlist.keys():
        dict_child_edges[station]=[]
        for child in dict_linkedlist[station]:
            s_edge=str([station,child])
            dict_child_edges[station].append(s_edge)
    return dict_child_edges

#test=djikstra10(results,'1')   #doesn't work
def djikstra10(mylist,start_station):
    dict_weighted=dic_weighted_edges(mylist)
    dict_linkedlist=dic(mylist)
    dict_previous_distance={}

    lS_unvisited=[start_station]
    lS_path=[]


    #create a dictionary initializing distances and previous station {[station]:[[distance],[previous]}
    for station in dict_linkedlist.keys():

        if station==start_station:
            dict_previous_distance[station]=[0]#initialize the distance at zero for the start station
        else:
            lS_unvisited.append(station)
            dict_previous_distance[station]=[None]
        dict_previous_distance[station].append(None)
    lS_unvisited.append(start_station)
    
    while lS_unvisited!=[]:
        s_current_search=lS_unvisited.pop()
        print('current_search='+str(s_current_search))
        lS_path.append(s_current_search)#append the current_search to the visited list
        
        s_min_child=None#initialize the child station with the minimum distance
        int_min_weight_child=None#initialize the minimum distance for child 
        
        #step1: update adjacent distances and previous
        for child in dict_linkedlist[s_current_search]:

            if child not in lS_unvisited:
                break
            else:#if not, update adjacent and previous
                s_current_edge=str([s_current_search,child])
                int_distance=dict_weighted[s_current_edge]
                dict_previous_distance[child][0]=int_distance
                dict_previous_distance[child][1]=s_current_search

        #step 2: choose the minimum distance between children
        for child in dict_linkedlist[s_current_search]:
            int_current_weight=dict_previous_distance[child][0]
            
            if child not in lS_unvisited:
                break
            else:
                if int_min_weight_child==None:
                    int_min_weight_child=int_current_weight
                    s_min_child=child
                else:
                    if int_current_weight<int_min_weight_child:#check i
                        int_min_weight_child=int_current_weight
                        s_min_child=child#retrive the path with the minimum distance
        
        #step3: indicate that the choosen child is visited and update the distance from source
            lS_path.append(s_min_child)
            del lS_unvisited[lS_unvisited.index(s_min_child)]#indicate that we have visited this child
        
        #step4: find the adjacents of the choosen child,calculate distance adj+adj2, and update dict_previous_distance
        
        for child2 in dict_linkedlist[s_min_child]:
            s_child2_edge=str([s_min_child,child2])
            int_added_distance=dict_previous_distance[s_min_child][0]+dict_weighted[s_child2_edge]
            s_current_child2=str([s_current_search,child2])
            if s_current_child2 not in dict_weighted.keys():
                dict_previous_distance[child2][0]=dict_weighted[s_child2_edge]
                dict_previous_distance[child2][1]=child
            else:
                if int_added_distance<dict_weighted[s_current_child2]:
                    dict_previous_distance[child2][0]=int_added_distance
                    dict_previous_distance[child2][1]=child
                else:
                    dict_previous_distance[child2][0]=dict_weighted[s_current_child2]
                    dict_previous_distance[child2][0]=dict_weighted[s_current_search]
                
        #step 5: choose the minimum distance between adjacent children (child2)
        
        int_min_distance_child2=None
        s_min_child2=None
        for child2 in dict_linkedlist[s_min_child]:
            if child not in lS_unvisited:
                break
            else: 
                if child2 not in lS_path:
                    if int_min_distance_child2==None:
                        int_min_distance_child2= dict_weighted[str([s_min_child,child2])]
                        s_min_child2=child2
                    else:
                        if dict_weighted[str([s_min_child,child2])]<int_min_distance_child2:
                            int_min_distance_child2=dict_weighted[str([s_min_child,child2])]
                            s_min_child2=child2
        
                lS_path.append(child2)
                print('unvisited='+str(lS_unvisited))
                del lS_unvisited[lS_unvisited.index(child2)]
                lS_unvisited.append(child2)
        
    return lS_path


###########################################################################################
###########################################################################################"
###############################################################################################"
#test=dic_edges_str_list(results)   {'[Station1,station2]'=[station1,station2]}
#len(test)=933
def dic_edges_str_list(mylist):
    lS_weighted_routes=prepare(mylist)
    dict_list_routes={}
    for line in lS_weighted_routes:
        sL_edge=str([line[0],line[1]])
        dict_list_routes[sL_edge]=[line[0],line[1]]
    return dict_list_routes

#test=dic_parents(results)  {'[station1,station2]':'[station0,station1]','[station22,station1]' etc...}
#len(test)=933
def dic_parents(mylist):
    dict_edges_transformed=dic_edges_str_list(mylist)
    dict_parents={}
    for edge in dict_edges_transformed:
        sL_station_values=dict_edges_transformed[edge]
        s_start_station=sL_station_values[0]
        for edge2 in dict_edges_transformed:
            sL_station_values2=dict_edges_transformed[edge2]
            s_end_station=sL_station_values2[1] 
            if s_start_station==s_end_station:
                if edge not in dict_parents.keys():
                    dict_parents[edge]=[edge2]
                else:
                    dict_parents[edge].append(edge2)
    return dict_parents

#test=dic_child(results)  {'[station1,station2]':'[station2,station3]','[station2,station365]' etc...}
#len(test)=933    
def dic_child(mylist):
    dict_edges_transformed=dic_edges_str_list(mylist)
    dict_child={}
    for edge in dict_edges_transformed:
        sL_station_values=dict_edges_transformed[edge]
        s_end_station=sL_station_values[1]
        for edge2 in dict_edges_transformed:
            sL_station_values2=dict_edges_transformed[edge2]
            s_start_station=sL_station_values2[0] 
            if s_start_station==s_end_station:
                if edge not in dict_child.keys():
                    dict_child[edge]=[edge2]
                else:
                    dict_child[edge].append(edge2)
    return dict_child


#test=dic_in_degrees_edges(results)
#len(test)=933
def dic_in_degrees_edges(mylist):#create a dictonary{weighted edge:nb in_degrees}
    dict_parent=dic_parents(mylist)
    dict_in_degrees={}
    for edge in dict_parent:
        lS_temp_values=dict_parent[edge]
        n_in_degrees=len(lS_temp_values)
        dict_in_degrees[edge]=n_in_degrees   
    
    return dict_in_degrees
    

#test=fibo(results,start="['99', '358']")    
def fibo(mylist,start):
    dict_w_edges=dic_weighted_edges(mylist)
    dict_child=dic_child(mylist)
    int_minh=min(dict_w_edges.values())
    dict_root_list={}
    dict_root_list[start]=dict_w_edges[start] 
    s_min_pointer=''
    
    dict_fibo={}
    dict_fibo[start]=[]
    
    #insert
        #create a new singleton

        #add to root list,update min pointer if necessary
    for edge in dict_w_edges.keys():
        s_min_value=min(dict_root_list.values())
        for root in dict_root_list:
            if dict_root_list[root]==s_min_value:
                s_current_root=root
            if dict_w_edges[edge]<s_min_value:
                s_min_value=dict_w_edges[edge]#delete min
                s_min_pointer=edge
                #make larger root be a child of smaller route
                #delete min, minds its children into root list
                if edge not in dict_fibo.keys():
                    dict_fibo[edge]=[start]
                    for child in dict_fibo[start]:
                        dict_root_list[child]=dict_w_edges[child]
                else:
                    dict_fibo[edge].append[start]
            else:
                dict_fibo[start].append(edge)

                    
        
    return dict_fibo.keys()

#test=find_min(results)    
def find_min(mylist):
    # A (ascending or min) priority queue keeps element with
    # lowest priority on top. So pop function pops out the element with
    # lowest value. It can be implemented as sorted or unsorted array
    # (dictionary in this case) or as a tree (lowest priority element is
    # root of tree)
    dict_w_edges=dic_weighted_edges(mylist)
    lowest = max(dict_w_edges.values())+1
    keylowest = None
    for key in dict_w_edges.keys():
        if dict_w_edges[key] < lowest:
            lowest = dict_w_edges[key]
            keylowest = key
    del dict_w_edges[keylowest]
    return keylowest
#test=dijkstra_test(results,"['99', '358']")   
def dijkstra_test(mylist, start):
    dict_w_edges=dic_weighted_edges(mylist)
    dict_child=dic_child(mylist)
    # Using priority queue to keep track of minium distance from start
    # to a vertex.
    pqueue = {} # vertex: distance to start
    dist = {}   # vertex: distance to start
    pred = {}   # vertex: previous (predecesor) vertex in shortest path
 
    # initializing dictionaries
    for edge in dict_w_edges.keys():
        dist[edge] = 1000
        pred[edge] = -1
    dist[start] = 0
    for edge in dict_w_edges.keys():
        pqueue[edge] = dist[edge] # equivalent to push into queue

    while pqueue!=[]:
        s_min = find_min(pqueue) # for priority queues, pop will get the element with smallest value
        for child in dict_child[s_min]: # for each neighbor of u
            weight = dict_w_edges[s_min][child] # distance u to v
            newdist = dist[s_min] + weight
            if (newdist < dist[child]): # is new distance shorter than one in dist?
                # found new shorter distance. save it
                pqueue[child] = newdist
                dist[child] = newdist
                pred[child] = s_min
 
    return dist, pred
#end="['77', '78']")
#test=Dijkstra(results,start="['99', '358']",end="['77', '78']")     
#test=Dijkstra2(results,start="['99', '358']")
def Dijkstra2(mylist,start):
    dict_w_edges=dic_weighted_edges(mylist)
    dict_child=dic_child(mylist)
    s_current_edge=start
    dict_distance={}
    int_infinite=max(dict_w_edges.values())+1
    sL_visited=[]
    
    #create a dictionary with all distances assigned to infinite, except start edge=0:
    for edge in dict_w_edges:
        if edge==s_current_edge:
            dict_distance[edge]=0
        else:    
            dict_distance[edge]=int_infinite

    #while all vertex are not in dict_distance:
    while len(sL_visited)!=len(dict_w_edges):
            #Pick a vertex u which is not there in sptSetand has minimum distance value
        for child in dict_child[s_current_edge]:
            print(sL_visited)
            sL_visited.append(child)
            int_distance_source=dict_distance[s_current_edge]
            int_distance_child=dict_w_edges[child]
            int_distance=int_distance_source+int_distance_child
            if dict_distance[child]==int_infinite:
                dict_distance[child]=int_distance
            else:
                if int_distance<dict_distance[child]:
                    dict_distance[child]=int_distance
            s_current_edge=child
    return dict_distance

        






#doesn't work
def Dijkstra(mylist,start,end,sL_shortest_path=[]):
    sL_shortest_path.append(start)
    dict_w_edges=dic_weighted_edges(mylist)
    dict_child=dic_child(mylist)
    s_current_node=start
    lS_child=dict_child[s_current_node]
    lS_child_weights=[]
    #print(sL_shortest_path)

    if lS_child_weights!=[]:
        s_min_weight=min(lS_child_weights)
    else:
        s_min_weight=max(dict_w_edges.values())
    
    while s_current_node!=end:
        for node in lS_child:
            lS_child_weights.append(dict_w_edges[node])
    
            for child in dict_child[s_current_node]:
                if child not in sL_shortest_path:
                    if dict_w_edges[child]<=s_min_weight:
                #print("min_weight="+str(s_min_weight))
                #sL_shortest_path=child
                        s_min_weight=dict_w_edges[child]
                        s_current_node=child
                        lS_child_weights=[]
                #print("current node="+s_current_node)
                        Dijkstra(mylist,start=s_current_node,end=end,sL_shortest_path=sL_shortest_path)
    return sL_shortest_path
        
        
    
    
    
    
    
    
    
#########################################################################"
#OK to compute the complexity and the run time  
#test=dic_out_degrees(results)  #create a dictionary{station:nb of out_degrees)}  
def dic_out_degrees(mylist):
    dS_linkedlist=dic(mylist)
    d_dic_out_degrees={}
    for station in dS_linkedlist:
        lS_temp_values=dS_linkedlist[station]
        n_out_degrees=len(lS_temp_values)
        d_dic_out_degrees[station]=n_out_degrees
        
    return d_dic_out_degrees
