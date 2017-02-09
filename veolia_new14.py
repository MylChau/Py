# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 21:36:49 2016

@author: Godzila
"""
'''
Variables naming:
    - l_xxx:list of different type
    - sL_xxx: list of strings
    - s_xxx: string
    - dict_xxx: dictionary
    - int_xxx: integer
    - bol_xxx: bolean

To get result: 
    valves_to_close2(broken_pipe,mylist)
    test30=valves_to_close2('14T11b7',l_network)
'''
'''Running time
test=runningtime('14T11b7',l_network)

Check with shorter list of pipe.
Create 3 lists: pipes=1,pipes=100,pipes=1000


Observations:n1=10,n=100(=n1**10) 
('time 10 pipes=--- 8.643138885498047 seconds ---',    n=10
 'time 100 pipes=--- 17.464409112930298 seconds ---',  around 2*(n=10)time 
 'time 1000 pipes=--- 26.136589288711548 seconds ---') around 3*(n=10)time

log(10)=1
log(10**2)=2log(10)=2
log(10**3)=  =>3log(10)=3

so O(logn)) seems ok
'''
'''
Step 0: import data
the path has to be changed manually to the directory where the file form Veolia is stored 
in the variable "s_path"

Variables:
        - l_network=list of the different lines in the orginal file
        - s_path: path to the directory where the file from Veolia is stored
'''

import os

cwd = os.getcwd()
s_path=r'C:\Users\Godzila\Documents\DSTI\Algorithms' 
os.chdir(s_path)

l_network = []
with open('water_network_txt.txt') as inputfile:
    for line in inputfile:
        l_network.append(line.strip().split())
'''
Step 1: I do a list of all valves and pipes(my edges) with nodes(vertex)
Step2: I do an adjacent list for my nodes
Step 3: I do a DFS in my adjacent list. When the DFS meets an edge that corresponds to a valve, it stop, register the edge and try an other path.
'''


'''Step 1: I do a list of all valves and pipes(my edges) with nodes(vertex) {edge:[node1,node2]} where edges are valves and pipes
Variables:
    int_pipes_lower_bound: find the index of the lower bound to consider in the global file for pipes
    int_pipes_upper_bound: find the index of the lower bound to consider in the global file for pipes
    int_valves_lower_bound: find the index of the lower bound to consider in the global file for valves
    int_valves_upper_bound: find the index of the lower bound to consider in the global file for valves
    sL_pipes: list of all lines in the original file related to pipes
    sL_valves: list of all lines in the original file related to valves
    sL_nodes_temp: temporary list aloowing to store node 1 and node 2
    dict_valves: linked list {valve:[node 1, node 2]}
    dict_pipes: linked list {pipe:[node 1, node 2]}
    
    return a linked list with all edges (pipes and valves) and their corresponding nodes
    {edge:[node1,node2]}
    '''

'''Order edges_with_vertex(mylist)
O(n)
'''
#test1=edges_with_vertex(l_network) 
#{edge:[node1,node2]} - edge is a pipe or a valve
#len test1=6902
def edges_with_vertex(mylist):
    #info concerning pipes are in liness between [PIPES] and [PUMPS]
    int_pipes_lower_bound=mylist.index(['[PIPES]'])+2#find "[PIPES]" then add2 to go to next line and skip header
    int_pipes_upper_bound=mylist.index(['[PUMPS]'])-2#find "[PUMPS]" then retrieve 2 to go to the last pipe
    sL_pipes=mylist[int_pipes_lower_bound:int_pipes_upper_bound]#create the list of pipes with attributes including node 1 and node 2
 
    #Create the dictionary
    dict_pipes={}#{pipe:[node1,node2]}
    for line in sL_pipes:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_pipes[line[0]]=sL_nodes_temp
    
    #same process to create the linked list for valves. Info concerning valves are between [VALVES] and [TAGS]
    int_valves_lower_bound=mylist.index(['[VALVES]'])+2
    int_valves_upper_bound=mylist.index(['[TAGS]'])-2
    sL_valves=mylist[int_valves_lower_bound:int_valves_upper_bound]#create the list of valves with attributes including node 1 and node 2

    #create the dictionary
    dict_valves={}
    for line in sL_valves:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_valves[line[0]]=sL_nodes_temp
    
    for valve in dict_valves.keys():
        dict_pipes[valve]=dict_valves[valve]
        
    return dict_pipes



'''Step2: I do an adjacent list for my nodes {node:[node1,node2...noden]}
Variables:
    - dict_edges: linked list {edge:[node1,node2]}
    - dict_nodes: final result {node:[node1,node2...noden]}
    - adjacent_nodes: temporary list to store adjacent nodes
    - int_index_node: to check if we are working on node 1 or node 1
    - int_index_other_node: 1 if int_index_node is 0, 0 if int_index_node is one

    return a linked list with all adjacent nodes for one node
    {node:[node1,node2,...noden]}                           
'''
'''
Order adjacent_list(mylist)
O(n)+O(n)=O(2n)=O(n)
'''
#{node:[node1,node2...]}
#test2=adjacent_list(l_network)
#'14T11b7'
#len test2=6449
def adjacent_list(mylist):
    dict_edges=edges_with_vertex(mylist)
    dict_nodes={}
    for nodes in dict_edges.values(): #to retrieve values of nodes for each edge - only two by edge
        adjacent_nodes_temp=[]
        for node in nodes:#for each nodes of the edge
            int_index_node=nodes.index(node)#check if it is the first or the second node
            if int_index_node==0:#if it is the first
                int_index_other_node=1#the other node is the second
            else:
                int_index_other_node=0# if not, the second node is the first
            if node not in dict_nodes.keys():#if this node is already in the adjacent list
                adjacent_nodes_temp.append(nodes[int_index_other_node])#I store it in the temporary node list
                dict_nodes[node]=adjacent_nodes_temp#the temporary node list become the adjacent values for my node
            else:
                dict_nodes[node].append(nodes[int_index_other_node])#if I already have adjacent values for my node, I just add this one
    return dict_nodes

'''Step 3: I do a DFS in my adjacent list. When the DFS meets an edge that corresponds to a valve, it stop, register the edge and try an other path.
Variables:
    - dict_nodes: adjacent list of my nodes
    - dict_all_valves: linked list {valve:[node 1, node 2]}
    - sL_valves_to_close_nodes: list of the nodes of the valves to close
    - sL_valves_to_close: list of the valves to close
    - sL_visited: list of the nodes visited
    - sL_stack:stack for dfs
    - s_current_search: the node that we are exploring, updated at each loop
    - sL_values: values of adjacent nodes of the current search node
    - sL_edge1 and sL_edge2: edge formed by the curent_search node and one of its adjcent node (in lS_values)
    - bol_check1 and bol_check2: bolean. True if the edge is an edge corresponding to a valve, otherwise false
    - sL_nodes_broken_pipes: nodes of the broken pipe
    - sL_first_path and sL_second_path: valves found from node 1 and node 2 of the broken pipe
    
    dict_valves(myliste) returns the linked list for valves {valve:[node1,node2]}
    my_dfs_with_valves(mylist, departure_node) returns a list containing the valves to close 
        (valves first encountered for each path in dfs for one node)
    valves_to_close2(broken_pipe,mylist) returns the valves to close for one pipe, consdering its two nodes

'''

'''    
order dict_valves(mylist):
O(n)

order my_dfs_with_valves(mylist,departure_node)
O(n)+O(n)+O(n)+O(nlogn)+O(n)=O(n(4+logn))=O(nlogn) 

valves_to_close2(broken_pipe,mylist)
O(n)+O(n)+O(logn)+O(logn)=O(2logn)=o(logn)  
'''

def dict_valves(mylist):#♣create the dictionary of valves
    int_valves_lower_bound=mylist.index(['[VALVES]'])+2
    int_valves_upper_bound=mylist.index(['[TAGS]'])-2
    sL_valves=mylist[int_valves_lower_bound:int_valves_upper_bound]
    dict_valves={}
    for line in sL_valves:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_valves[line[0]]=sL_nodes_temp
    return dict_valves

    #test_40=my_dfs_with_valves(l_network,'14N353e')
#len(test_40)=98
def my_dfs_with_valves(mylist,departure_node):#return the valves to close
    dict_nodes=adjacent_list(mylist)#adjacent list nodes {node:[node1,node2]}
    dict_all_valves=dict_valves(mylist)#linkedlist valves {valve:[node1,node2]}
    dict_full_list=edges_with_vertex(mylist) #linked list with all edges (pipes and valves) {edge:[node1,node2]}
    sL_valves_to_close_nodes=[]#list of nodes of valves to close
    sL_valves_to_close=[]#list of valves to close
    sL_visited=[departure_node]#list of visited nodes, initialized with departure node
    sL_stack=[]#stack for dfs
    for nodes in dict_nodes[departure_node]:
        sL_stack.append(nodes)#we append the stack with the two nodes adjacent to the staring node
    while sL_stack!=[]:#while stack not empty
        s_current_search=sL_stack.pop()#s_current search is the last value of the stack
        if s_current_search not in sL_visited: #if current search has not been visited yet
            sL_visited.append(s_current_search)#add the current search to visited
            if s_current_search in dict_nodes.keys():#if the current search is a key in dict_nodes, means that it has adjacent nodes
                sL_values=dict_nodes[s_current_search]#sL_values is a list of the nodes adjacents to the current search
                for value in sL_values:#for adjacent node in list of adjacent nodes
                    sL_edge1=[s_current_search,value]#edge between the current search and his adjacent
                    bol_check1=sL_edge1 in dict_all_valves.values()#check if the edge is a valve (if it appears in the valves list)
                    if bol_check1==True:#if it is a valve
                        sL_valves_to_close_nodes.append(sL_edge1)#add it to the list of edges of valves to close
                    break#don't need to check if the inverse edge is Thrue - cut the path not append the stack with the value
                    sL_edge2=[s_current_search,value]#same thing we the inverse edge, has the graph is not directed
                    bol_check2=sL_edge2 in dict_all_valves.values()
                    if bol_check2==True:
                        sL_valves_to_close_nodes.append(sL_edge2)
                    break#cut the path not appending the stack with the value - go to next path
                    sL_stack.append(value)#add the node to the stack
                    
    #associate the list of edges found to the valves ID
    for edge in sL_valves_to_close_nodes: #for edges in the valves_to_close_nodes list
        for key in dict_full_list.keys():# for each edge in the linked list of all edges
            if dict_full_list[key]==edge:#check if the edges correspond to valves edge - not the most efficient way, but couldn't find how to write the code otherwise...
                sL_valves_to_close.append(key)#add the valveID to the valveID list   
    
    return sL_valves_to_close

#test30=valves_to_close2('14T11b7',l_network)
#len(test30)=199    
def valves_to_close2(broken_pipe,mylist):
    dict_edges=edges_with_vertex(mylist)#linked list for all edges
    sL_nodes_broken_pipes=dict_edges[broken_pipe]#nodes for the broken pipe
    sL_first_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[0])#valves to close for the first node
    sL_second_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[1])# valves to close for the second node
    for valve in sL_second_path:
        if valve not in sL_first_path:
            sL_first_path.append(valve)#append to the valves to close for the first node the valves to close for the second node if they are not already in the list
    return sL_first_path

    
##############################################################################################
'''Running time

Check with shorter list of pipe.
Create 3 lists: pipes=1,pipes=100,pipes=1000

('time 10 pipes=--- 8.643138885498047 seconds ---',  
 'time 100 pipes=--- 17.464409112930298 seconds ---',  around 2 
 'time 1000 pipes=--- 26.136589288711548 seconds ---') around 1.49

Around double for n*10
10log10=10
100log100=200   around 20
1000log1000=3000     around 15
linear y for exponential x--logarithmic function y=logx
so O(nlogn)) seems ok
'''
#test=runningtime('14T11b7',l_network)
def runningtime(broken_pipe,mylist):
    import time
    start_time = time.time()
    func_function10=valves_to_close210(broken_pipe,mylist)
    time10=("--- %s seconds ---" % (time.time() - start_time))
    func_function100=valves_to_close2100(broken_pipe,mylist)
    time100=("--- %s seconds ---" % (time.time() - start_time))
    func_function1000=valves_to_close21000(broken_pipe,mylist)
    time1000=("--- %s seconds ---" % (time.time() - start_time))
    return('time 10 pipes='+str(time10),'time 100 pipes='+str(time100),'time 1000 pipes='+str(time1000))

def edges_with_vertex10(mylist):
    #info concerning pipes are in liness between [PIPES] and [PUMPS]
    int_pipes_lower_bound=mylist.index(['[PIPES]'])+2#find "[PIPES]" then add1 to go to next line
    int_pipes_upper_bound=mylist.index(['[PIPES]'])+12#find "[PUMPS]" then retrieve 2 to go to the last pipe
    sL_pipes=mylist[int_pipes_lower_bound:int_pipes_upper_bound]#create the list of pipes with attributes including node 1 and node 2
 
    #Create the dictionary
    dict_pipes={}#{pipe:[node1,node2]}
    for line in sL_pipes:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_pipes[line[0]]=sL_nodes_temp
    
    #same process to create the linked list for valves. Info concerning valves are between [VALVES] and [TAGS]
    int_valves_lower_bound=mylist.index(['[VALVES]'])+2
    int_valves_upper_bound=mylist.index(['[TAGS]'])-2
    sL_valves=mylist[int_valves_lower_bound:int_valves_upper_bound]#create the list of valves with attributes including node 1 and node 2

    #create the dictionary
    dict_valves={}
    for line in sL_valves:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_valves[line[0]]=sL_nodes_temp
    
    for valve in dict_valves.keys():
        dict_pipes[valve]=dict_valves[valve]
        
    return dict_pipes

def edges_with_vertex100(mylist):
    #info concerning pipes are in liness between [PIPES] and [PUMPS]
    int_pipes_lower_bound=mylist.index(['[PIPES]'])+2#find "[PIPES]" then add1 to go to next line
    int_pipes_upper_bound=mylist.index(['[PIPES]'])+102#find "[PUMPS]" then retrieve 2 to go to the last pipe
    sL_pipes=mylist[int_pipes_lower_bound:int_pipes_upper_bound]#create the list of pipes with attributes including node 1 and node 2
 
    #Create the dictionary
    dict_pipes={}#{pipe:[node1,node2]}
    for line in sL_pipes:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_pipes[line[0]]=sL_nodes_temp
    
    #same process to create the linked list for valves. Info concerning valves are between [VALVES] and [TAGS]
    int_valves_lower_bound=mylist.index(['[VALVES]'])+2
    int_valves_upper_bound=mylist.index(['[TAGS]'])-2
    sL_valves=mylist[int_valves_lower_bound:int_valves_upper_bound]#create the list of valves with attributes including node 1 and node 2

    #create the dictionary
    dict_valves={}
    for line in sL_valves:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_valves[line[0]]=sL_nodes_temp
    
    for valve in dict_valves.keys():
        dict_pipes[valve]=dict_valves[valve]
        
    return dict_pipes

def edges_with_vertex1000(mylist):
    #info concerning pipes are in liness between [PIPES] and [PUMPS]
    int_pipes_lower_bound=mylist.index(['[PIPES]'])+2#find "[PIPES]" then add1 to go to next line
    int_pipes_upper_bound=mylist.index(['[PIPES]'])+1002#find "[PUMPS]" then retrieve 2 to go to the last pipe
    sL_pipes=mylist[int_pipes_lower_bound:int_pipes_upper_bound]#create the list of pipes with attributes including node 1 and node 2
 
    #Create the dictionary
    dict_pipes={}#{pipe:[node1,node2]}
    for line in sL_pipes:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_pipes[line[0]]=sL_nodes_temp
    
    #same process to create the linked list for valves. Info concerning valves are between [VALVES] and [TAGS]
    int_valves_lower_bound=mylist.index(['[VALVES]'])+2
    int_valves_upper_bound=mylist.index(['[TAGS]'])-2
    sL_valves=mylist[int_valves_lower_bound:int_valves_upper_bound]#create the list of valves with attributes including node 1 and node 2

    #create the dictionary
    dict_valves={}
    for line in sL_valves:
        sL_nodes_temp=[]
        sL_nodes_temp.append(line[1])
        sL_nodes_temp.append(line[2])
        dict_valves[line[0]]=sL_nodes_temp
    
    for valve in dict_valves.keys():
        dict_pipes[valve]=dict_valves[valve]
        
    return dict_pipes
    
def adjacent_list10(mylist):
    dict_edges=edges_with_vertex1(mylist)
    dict_nodes={}
    for nodes in dict_edges.values(): #to retrieve values of nodes for each edge - only two by edge
        adjacent_nodes_temp=[]
        for node in nodes:#for each nodes of the edge
            int_index_node=nodes.index(node)#check if it is the first or the second node
            if int_index_node==0:#if it is the first
                int_index_other_node=1#the other node is the second
            else:
                int_index_other_node=0# if not, the second node is the first
            if node not in dict_nodes.keys():#if this node is already in the adjacent list
                adjacent_nodes_temp.append(nodes[int_index_other_node])#I store it in the temporary node list
                dict_nodes[node]=adjacent_nodes_temp#the temporary node list become the adjacent values for my node
            else:
                dict_nodes[node].append(nodes[int_index_other_node])#if I already have adjacent values for my node, I just add this one
    return dict_nodes
    
def adjacent_list100(mylist):
    dict_edges=edges_with_vertex100(mylist)
    dict_nodes={}
    for nodes in dict_edges.values(): #to retrieve values of nodes for each edge - only two by edge
        adjacent_nodes_temp=[]
        for node in nodes:#for each nodes of the edge
            int_index_node=nodes.index(node)#check if it is the first or the second node
            if int_index_node==0:#if it is the first
                int_index_other_node=1#the other node is the second
            else:
                int_index_other_node=0# if not, the second node is the first
            if node not in dict_nodes.keys():#if this node is already in the adjacent list
                adjacent_nodes_temp.append(nodes[int_index_other_node])#I store it in the temporary node list
                dict_nodes[node]=adjacent_nodes_temp#the temporary node list become the adjacent values for my node
            else:
                dict_nodes[node].append(nodes[int_index_other_node])#if I already have adjacent values for my node, I just add this one
    return dict_nodes
    
def adjacent_list1000(mylist):
    dict_edges=edges_with_vertex1000(mylist)
    dict_nodes={}
    for nodes in dict_edges.values(): #to retrieve values of nodes for each edge - only two by edge
        adjacent_nodes_temp=[]
        for node in nodes:#for each nodes of the edge
            int_index_node=nodes.index(node)#check if it is the first or the second node
            if int_index_node==0:#if it is the first
                int_index_other_node=1#the other node is the second
            else:
                int_index_other_node=0# if not, the second node is the first
            if node not in dict_nodes.keys():#if this node is already in the adjacent list
                adjacent_nodes_temp.append(nodes[int_index_other_node])#I store it in the temporary node list
                dict_nodes[node]=adjacent_nodes_temp#the temporary node list become the adjacent values for my node
            else:
                dict_nodes[node].append(nodes[int_index_other_node])#if I already have adjacent values for my node, I just add this one
    return dict_nodes

def my_dfs_with_valves10(mylist,departure_node):#return the valves to close
    dict_nodes=adjacent_list(mylist)#adjacent list nodes {node:[node1,node2]}
    dict_all_valves=dict_valves(mylist)#linkedlist valves {valve:[node1,node2]}
    dict_full_list=edges_with_vertex10(mylist) #linked list with all edges (pipes and valves) {edge:[node1,node2]}
    sL_valves_to_close_nodes=[]#list of nodes of valves to close
    sL_valves_to_close=[]#list of valves to close
    sL_visited=[departure_node]#list of visited nodes, initialized with departure node
    sL_stack=[]#stack for dfs
    for nodes in dict_nodes[departure_node]:
        sL_stack.append(nodes)#we append the stack with the two nodes adjacent to the staring node
    while sL_stack!=[]:#while stack not empty
        s_current_search=sL_stack.pop()#s_current search is the last value of the stack
        if s_current_search not in sL_visited: #if current search has not been visited yet
            sL_visited.append(s_current_search)#add the current search to visited
            if s_current_search in dict_nodes.keys():#if the current search is a key in dict_nodes, means that it has adjacent nodes
                sL_values=dict_nodes[s_current_search]#sL_values is a list of the nodes adjacents to the current search
                for value in sL_values:#for adjacent node in list of adjacent nodes
                    sL_edge1=[s_current_search,value]#edge between the current search and his adjacent
                    bol_check1=sL_edge1 in dict_all_valves.values()#check if the edge is a valve (if it appears in the valves list)
                    if bol_check1==True:#if it is a valve
                        sL_valves_to_close_nodes.append(sL_edge1)#add it to the list of edges of valves to close
                        break#don't need to check if the inverse edge is Thrue
                    sL_edge2=[s_current_search,value]#same thing we the inverse edge, has the graph is not directed
                    bol_check2=sL_edge2 in dict_all_valves.values()
                    if bol_check2==True:
                        sL_valves_to_close_nodes.append(sL_edge2)
                        break
                    sL_stack.append(value)#add the node to the stack
    #associate the list of edges found to the valves ID
    for edge in sL_valves_to_close_nodes: #for edges in the valves_to_close_nodes list
        for key in dict_full_list.keys():# for each edge in the linked list of all edges
            if dict_full_list[key]==edge:#check if the edges correspond to valves edge - not the most efficient way, but couldn't find how to write the code otherwise...
                sL_valves_to_close.append(key)#add the valveID to the valveID list   
    
    return sL_valves_to_close

#test30=valves_to_close2('14T11b7',l_network)
#len(test30)=199    
def valves_to_close210(broken_pipe,mylist):
    dict_edges=edges_with_vertex10(mylist)#linked list for all edges
    sL_nodes_broken_pipes=dict_edges[broken_pipe]#nodes for the broken pipe
    sL_first_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[0])#valves to close for the first node
    sL_second_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[1])# valves to close for the second node
    for valve in sL_second_path:
        if valve not in sL_first_path:
            sL_first_path.append(valve)#append to the valves to close for the first node the valves to close for the second node if they are not already in the list
    return sL_first_path
    
def my_dfs_with_valves100(mylist,departure_node):#return the valves to close
    dict_nodes=adjacent_list(mylist)#adjacent list nodes {node:[node1,node2]}
    dict_all_valves=dict_valves(mylist)#linkedlist valves {valve:[node1,node2]}
    dict_full_list=edges_with_vertex100(mylist) #linked list with all edges (pipes and valves) {edge:[node1,node2]}
    sL_valves_to_close_nodes=[]#list of nodes of valves to close
    sL_valves_to_close=[]#list of valves to close
    sL_visited=[departure_node]#list of visited nodes, initialized with departure node
    sL_stack=[]#stack for dfs
    for nodes in dict_nodes[departure_node]:
        sL_stack.append(nodes)#we append the stack with the two nodes adjacent to the staring node
    while sL_stack!=[]:#while stack not empty
        s_current_search=sL_stack.pop()#s_current search is the last value of the stack
        if s_current_search not in sL_visited: #if current search has not been visited yet
            sL_visited.append(s_current_search)#add the current search to visited
            if s_current_search in dict_nodes.keys():#if the current search is a key in dict_nodes, means that it has adjacent nodes
                sL_values=dict_nodes[s_current_search]#sL_values is a list of the nodes adjacents to the current search
                for value in sL_values:#for adjacent node in list of adjacent nodes
                    sL_edge1=[s_current_search,value]#edge between the current search and his adjacent
                    bol_check1=sL_edge1 in dict_all_valves.values()#check if the edge is a valve (if it appears in the valves list)
                    if bol_check1==True:#if it is a valve
                        sL_valves_to_close_nodes.append(sL_edge1)#add it to the list of edges of valves to close
                        break#don't need to check if the inverse edge is Thrue
                    sL_edge2=[s_current_search,value]#same thing we the inverse edge, has the graph is not directed
                    bol_check2=sL_edge2 in dict_all_valves.values()
                    if bol_check2==True:
                        sL_valves_to_close_nodes.append(sL_edge2)
                        break
                    sL_stack.append(value)#add the node to the stack
    #associate the list of edges found to the valves ID
    for edge in sL_valves_to_close_nodes: #for edges in the valves_to_close_nodes list
        for key in dict_full_list.keys():# for each edge in the linked list of all edges
            if dict_full_list[key]==edge:#check if the edges correspond to valves edge - not the most efficient way, but couldn't find how to write the code otherwise...
                sL_valves_to_close.append(key)#add the valveID to the valveID list   
    
    return sL_valves_to_close

#test30=valves_to_close2('14T11b7',l_network)
#len(test30)=199    
def valves_to_close2100(broken_pipe,mylist):
    dict_edges=edges_with_vertex100(mylist)#linked list for all edges
    sL_nodes_broken_pipes=dict_edges[broken_pipe]#nodes for the broken pipe
    sL_first_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[0])#valves to close for the first node
    sL_second_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[1])# valves to close for the second node
    for valve in sL_second_path:
        if valve not in sL_first_path:
            sL_first_path.append(valve)#append to the valves to close for the first node the valves to close for the second node if they are not already in the list
    return sL_first_path
    
def valves_to_close210(broken_pipe,mylist):
    dict_edges=edges_with_vertex10(mylist)#linked list for all edges
    sL_nodes_broken_pipes=dict_edges[broken_pipe]#nodes for the broken pipe
    sL_first_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[0])#valves to close for the first node
    sL_second_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[1])# valves to close for the second node
    for valve in sL_second_path:
        if valve not in sL_first_path:
            sL_first_path.append(valve)#append to the valves to close for the first node the valves to close for the second node if they are not already in the list
    return sL_first_path
    
def my_dfs_with_valves1000(mylist,departure_node):#return the valves to close
    dict_nodes=adjacent_list(mylist)#adjacent list nodes {node:[node1,node2]}
    dict_all_valves=dict_valves(mylist)#linkedlist valves {valve:[node1,node2]}
    dict_full_list=edges_with_vertex1000(mylist) #linked list with all edges (pipes and valves) {edge:[node1,node2]}
    sL_valves_to_close_nodes=[]#list of nodes of valves to close
    sL_valves_to_close=[]#list of valves to close
    sL_visited=[departure_node]#list of visited nodes, initialized with departure node
    sL_stack=[]#stack for dfs
    for nodes in dict_nodes[departure_node]:
        sL_stack.append(nodes)#we append the stack with the two nodes adjacent to the staring node
    while sL_stack!=[]:#while stack not empty
        s_current_search=sL_stack.pop()#s_current search is the last value of the stack
        if s_current_search not in sL_visited: #if current search has not been visited yet
            sL_visited.append(s_current_search)#add the current search to visited
            if s_current_search in dict_nodes.keys():#if the current search is a key in dict_nodes, means that it has adjacent nodes
                sL_values=dict_nodes[s_current_search]#sL_values is a list of the nodes adjacents to the current search
                for value in sL_values:#for adjacent node in list of adjacent nodes
                    sL_edge1=[s_current_search,value]#edge between the current search and his adjacent
                    bol_check1=sL_edge1 in dict_all_valves.values()#check if the edge is a valve (if it appears in the valves list)
                    if bol_check1==True:#if it is a valve
                        sL_valves_to_close_nodes.append(sL_edge1)#add it to the list of edges of valves to close
                        break#don't need to check if the inverse edge is Thrue
                    sL_edge2=[s_current_search,value]#same thing we the inverse edge, has the graph is not directed
                    bol_check2=sL_edge2 in dict_all_valves.values()
                    if bol_check2==True:
                        sL_valves_to_close_nodes.append(sL_edge2)
                        break
                    sL_stack.append(value)#add the node to the stack
    #associate the list of edges found to the valves ID
    for edge in sL_valves_to_close_nodes: #for edges in the valves_to_close_nodes list
        for key in dict_full_list.keys():# for each edge in the linked list of all edges
            if dict_full_list[key]==edge:#check if the edges correspond to valves edge - not the most efficient way, but couldn't find how to write the code otherwise...
                sL_valves_to_close.append(key)#add the valveID to the valveID list   
    
    return sL_valves_to_close

#test30=valves_to_close2('14T11b7',l_network)
#len(test30)=199    
def valves_to_close21000(broken_pipe,mylist):
    dict_edges=edges_with_vertex1000(mylist)#linked list for all edges
    sL_nodes_broken_pipes=dict_edges[broken_pipe]#nodes for the broken pipe
    sL_first_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[0])#valves to close for the first node
    sL_second_path=my_dfs_with_valves(mylist,sL_nodes_broken_pipes[1])# valves to close for the second node
    for valve in sL_second_path:
        if valve not in sL_first_path:
            sL_first_path.append(valve)#append to the valves to close for the first node the valves to close for the second node if they are not already in the list
    return sL_first_path
############################################################################################
#Test scripts!
#DO NOT COMPUTE THE COMPLEXITY! JUST A TEST!
#test_mydfs=my_dfs(l_network,'14N353e')
#len(test_my_dfs)=6444 it works yeaaaaaah!
def my_dfs(mylist,departure_node):
    dict_nodes=adjacent_list(mylist)
    dict_all_valves=dict_valves(mylist)
    dict_full_list=edges_with_vertex(mylist)
    sL_valves_to_close_nodes=[]
    sL_valves_to_close=[]
    sL_visited=[]
    stack=[]
    visited=[]
    stack=[]
    visited=[departure_node]
    for nodes in dict_nodes[departure_node]:
        stack.append(nodes)
    while stack!=[]:
        #print('step1'+str(stack))
        current_search=stack.pop()
        if current_search not in visited:
            visited.append(current_search)
            #print('step1bis'+str(visited))
            if current_search in dict_nodes.keys():
                #print('step2 node_key'+str(current_search))
                values=dict_nodes[current_search]
                #print('step2bis_values_tree'+str(values))
                for value in values:
                    #print('step3_value'+str(value))
                    stack.append(value)
                    #print('step4_stack'+str(stack))
    return visited

#test50=multiple_pipes(l_network,['14T11b7','14T11b6','14T11b5'])
def multiple_pipes(mylist,list_pipes_broken):
    import time
    start_time = time.time()
    lS_all_valves=[]
    for pipe in list_pipes_broken:
        lS_valves_multiple=valves_to_close2(pipe,mylist)
        lS_all_valves.append(lS_valves_multiple)
    print("--- %s seconds ---" % (time.time() - start_time))
    return lS_all_valves

#JUST A TEST NOT PART OF THE FINAL ALGORITHM - DO NOT COUNT FOR COMPLEXITY    
#test nb unique nodes in list: 6449
    #test11=test_nb_nodes(l_network)
def test_nb_nodes(mylist):
    dict_edges=edges_with_vertex(mylist)
    lS_nodes=[]
    count=0
    for value in dict_edges.values():
        for node in value:
            if node not in lS_nodes:
               lS_nodes.append(node) 
               count+=1
    return count        



    

        