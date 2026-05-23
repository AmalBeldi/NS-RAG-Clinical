import networkx as nx
def witness_graph(g,supported):
    keep=set()
    for n,a in g.nodes(data=True):
        label=str(a.get('label','')).lower(); val=str(a.get('value','')).lower()
        for s in supported:
            low=s.lower()
            if (label and label in low) or (val and val in low):
                keep.add(n); keep.update([u for u,_ in g.in_edges(n)]); keep.update([v for _,v in g.out_edges(n)])
    return g.subgraph(keep).copy() if keep else nx.MultiDiGraph()
def minimal_explanation_graph(wg): return wg.subgraph([n for n,a in wg.nodes(data=True) if a.get('type')!='Time']).copy()
def explanation_sizes(wg,mg): return {'g_exp_size':wg.number_of_nodes()+wg.number_of_edges(),'g_min_size':mg.number_of_nodes()+mg.number_of_edges()}
