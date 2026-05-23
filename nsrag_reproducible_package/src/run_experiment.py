import argparse,sys
from pathlib import Path
import pandas as pd
from tqdm import tqdm
sys.path.append(str(Path(__file__).resolve().parent))
from utils import load_jsonl,ensure_dir
from pipeline import run_method
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out',default='results'); a=p.parse_args(); ensure_dir(a.out); ensure_dir(f'{a.out}/tables')
records=load_jsonl(a.input); methods=['llm_no_context','textual_rag','graph_linearization','ns_rag_no_verify','ns_rag_no_minimal','ns_rag_full']; rows=[]
for rec in tqdm(records,desc='benchmark'):
    for m in methods: rows.append(run_method(rec,m,'summarization',''))
    for qa in rec.get('qa_pairs',[]):
        for m in methods: rows.append(run_method(rec,m,'qa',qa['question']))
df=pd.DataFrame(rows); df.to_csv(f'{a.out}/experiment_results.csv',index=False)
summary=df.groupby(['method','task'])[['fact_f1','hallucination_rate','explanation_coverage','minimality_ratio','verification_success_rate','context_tokens']].mean().reset_index(); summary.to_csv(f'{a.out}/summary_results.csv',index=False); summary.to_latex(f'{a.out}/tables/main_results.tex',index=False,float_format='%.3f')
gs=df.groupby(['method','task'])[['dg_nodes','dg_edges','gs_nodes','gs_edges','rdf_triples','context_tokens']].mean().reset_index(); gs.to_csv(f'{a.out}/patient_graph_stats.csv',index=False); gs.to_latex(f'{a.out}/tables/graph_stats.tex',index=False,float_format='%.1f')
rt=df.groupby(['method','task'])[[c for c in df.columns if c.startswith('time_')]].mean().reset_index(); rt.to_csv(f'{a.out}/runtime.csv',index=False); rt.to_latex(f'{a.out}/tables/runtime.tex',index=False,float_format='%.4f')
print(summary)
