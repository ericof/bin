#!/usr/local/bin/python2.4
"""
An example using Graph as a weighted network.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
from fbook import ff

x_min,x_max = (0.946,1.3)
y_min,y_max = (0.9,1.3)
x_avg = (x_max+x_min)/2
y_avg = (y_max+y_min)/2


amigos = dict([(f.get('uid'),(f.get('name'),len(f.get('friends')))) for f in ff])
edges = [(ffi.get('uid'), [f.get('uid') for f in ffi.get('friends')]) for ffi in ff]
edges = [(len(edge[1]),edge) for edge in edges]
edges.sort()
edges.reverse()
edges = [edge[1] for edge in edges]
G=nx.Graph()
G.add_nodes_from(amigos.keys())

processed = []
for f,frFs in edges:
    processed.append(f)
    tmpAmigos = len(frFs)
    for frF in frFs:
        tmpAmigosAmigo = amigos[frF][1]
        if not frF in processed:
            print tmpAmigosAmigo, tmpAmigos, tmpAmigosAmigo/(float(tmpAmigos) ** 2)
            G.add_edge(f,frF,weight=tmpAmigosAmigo/(float(tmpAmigos) ** 2))

pos=nx.spring_layout(G,iterations=500,scale=2.2) # positions for all nodes
ncenter = processed[0]
p=nx.single_source_shortest_path_length(G,ncenter)
node_sizes = [int(len(G.neighbors(k))/3 + 2) for k in pos.keys()]
print min(node_sizes),max(node_sizes), set(node_sizes)
#print pos
#plt.figure(figsize=(8,8))

nx.draw_networkx_nodes(G,pos,nodelist=pos.keys(),
                       node_size=node_sizes,
                       node_color=[p.get(c,7) for c in pos.keys()],
                       cmap=plt.cm.Reds_r)
nx.draw_networkx_edges(G,pos,nodelist=[ncenter],width=1,alpha=0.2)


# labels
labels = dict([(k,v[0]) for k,v in amigos.items() if v[1]>40])
nx.draw_networkx_labels(G,pos,labels = labels, font_size=12,font_family='Verdana')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.axis('on')

plt.savefig("weighted_graph.png") # save as png
plt.show() # display
