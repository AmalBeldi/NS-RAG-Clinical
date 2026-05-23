import networkx as nx

def build_patient_graph(record):
    g=nx.MultiDiGraph(); pid=record['patient_id']; g.add_node(pid,type='Patient',label=pid)
    for dx in record.get('diagnoses',[]):
        n=f'DX::{dx}'; g.add_node(n,type='Diagnosis',label=dx); g.add_edge(pid,n,relation='hasDiagnosis')
    for med in record.get('medications',[]):
        n=f'MED::{med}'; g.add_node(n,type='Medication',label=med); g.add_edge(pid,n,relation='hasMedication')
    for lab in record.get('labs',[]):
        n=f"LAB::{lab['name']}::{lab.get('date','NA')}"; g.add_node(n,type='Lab',label=lab['name'],value=lab['value'],unit=lab.get('unit',''),date=lab.get('date',''))
        g.add_edge(pid,n,relation='hasLab'); t=f"TIME::{lab.get('date','NA')}"; g.add_node(t,type='Time',label=lab.get('date','')); g.add_edge(n,t,relation='measuredAt')
    for ev in record.get('events',[]):
        n=f"EVENT::{ev.get('type','event')}::{ev.get('date','NA')}"; g.add_node(n,type='Event',label=ev.get('label',''),date=ev.get('date','')); g.add_edge(pid,n,relation='hasEvent')
    return g

def summarize_graph(g, question='', max_neighbors=3):
    if not question: return g.copy()
    q=question.lower(); keep=set([n for n,d in g.nodes(data=True) if d.get('type')=='Patient'])
    for n,d in g.nodes(data=True):
        label=str(d.get('label','')).lower(); typ=str(d.get('type','')).lower(); val=str(d.get('value','')).lower()
        if any(tok in label or tok in typ or tok in val for tok in q.split()): keep.add(n)
    exp=set(keep)
    for n in list(keep):
        exp.update(v for _,v in g.out_edges(n)); exp.update(u for u,_ in g.in_edges(n))
    if len(exp)<=1:
        for p in keep: exp.update(v for _,v in list(g.out_edges(p))[:max_neighbors*4])
    return g.subgraph(exp).copy()

def graph_stats(g): return {'nodes':g.number_of_nodes(),'edges':g.number_of_edges()}

def linearize_graph(g, max_lines=80):
    lines=[]
    for u,v,data in g.edges(data=True):
        rel=data.get('relation','relatedTo'); su=g.nodes[u].get('label',u); sv=g.nodes[v].get('label',v)
        if g.nodes[v].get('type')=='Lab': sv=f"{sv}={g.nodes[v].get('value')} {g.nodes[v].get('unit')} on {g.nodes[v].get('date')}"
        lines.append(f"{su} --{rel}--> {sv}")
    return '\n'.join(lines[:max_lines])
