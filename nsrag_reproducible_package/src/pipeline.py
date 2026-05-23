import time
from graph_builder import build_patient_graph,summarize_graph,linearize_graph,graph_stats
from rdf_converter import nx_to_rdf,rdf_triples_count
from retrieval import textual_rag_context,graph_context
from generation import DeterministicClinicalGenerator,build_prompt
from verification import extract_assertions,verify_assertions,verification_status
from explainability import witness_graph,minimal_explanation_graph,explanation_sizes
from metrics import precision,recall,f1,hallucination_rate,explanation_coverage,minimality_ratio,verification_success
gen=DeterministicClinicalGenerator()
def reference_answer(record,task,question=''):
    if task=='summarization':
        parts=record.get('diagnoses',[])+record.get('medications',[])+[f"{l.get('name')} {l.get('value')}" for l in record.get('labs',[])]
        return '. '.join(parts)
    for qa in record.get('qa_pairs',[]):
        if qa['question']==question: return qa['reference_answer']
    return ''
def run_method(record,method,task,question=''):
    times={}; t=time.perf_counter(); g=build_patient_graph(record); times['graph_construction']=time.perf_counter()-t
    t=time.perf_counter(); gs=summarize_graph(g,question); times['graph_summarization']=time.perf_counter()-t
    t=time.perf_counter(); rdf=nx_to_rdf(gs); times['rdf_transformation']=time.perf_counter()-t
    if method=='llm_no_context': ctx=''
    elif method=='textual_rag': ctx=textual_rag_context(record,question or 'summary')
    else: ctx=graph_context(linearize_graph(gs))
    t=time.perf_counter(); out=gen.generate(build_prompt(task,question,ctx)); times['generation']=time.perf_counter()-t
    pred=extract_assertions(out); ref=extract_assertions(reference_answer(record,task,question))
    t=time.perf_counter(); sup,uns=verify_assertions(pred,record) if method!='llm_no_context' and method!='textual_rag' else ([],pred); times['verification']=time.perf_counter()-t
    status=verification_status(len(sup)/max(len(pred),1)) if sup or method.startswith('ns') or method=='graph_linearization' else 'NA'
    wg_size=mg_size=0
    t=time.perf_counter()
    if method in {'ns_rag_full','ns_rag_no_minimal'}:
        wg=witness_graph(gs,sup); mg=wg if method=='ns_rag_no_minimal' else minimal_explanation_graph(wg); sizes=explanation_sizes(wg,mg); wg_size=sizes['g_exp_size']; mg_size=sizes['g_min_size']
    times['explanation']=time.perf_counter()-t
    p=precision(pred,ref); r=recall(pred,ref); dg=graph_stats(g); sg=graph_stats(gs)
    return {'patient_id':record['patient_id'],'method':method,'task':task,'question':question,'output':out,'fact_precision':p,'fact_recall':r,'fact_f1':f1(p,r),'hallucination_rate':hallucination_rate(pred,sup),'explanation_coverage':explanation_coverage(pred,sup),'minimality_ratio':minimality_ratio(mg_size,wg_size),'verification_success_rate':verification_success(status),'status':status,'context_tokens':len(ctx.split()),'g_exp_size':wg_size,'g_min_size':mg_size,'dg_nodes':dg['nodes'],'dg_edges':dg['edges'],'gs_nodes':sg['nodes'],'gs_edges':sg['edges'],'rdf_triples':rdf_triples_count(rdf), **{f'time_{k}':v for k,v in times.items()}}
