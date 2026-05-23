import argparse,sys
from pathlib import Path
import pandas as pd
from tqdm import tqdm
sys.path.append(str(Path(__file__).resolve().parent))
from utils import load_jsonl,ensure_dir
from pipeline import run_method
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out',default='results'); a=p.parse_args(); ensure_dir(a.out); ensure_dir(f'{a.out}/tables')
records=load_jsonl(a.input); variants=['ns_rag_no_verify','graph_linearization','ns_rag_no_minimal','ns_rag_full']; rows=[]
for rec in tqdm(records,desc='ablation'):
    for qa in rec.get('qa_pairs',[]):
        for v in variants: rows.append(run_method(rec,v,'qa',qa['question']))
df=pd.DataFrame(rows); df.to_csv(f'{a.out}/ablation_results.csv',index=False)
summary=df.groupby('method')[['fact_f1','hallucination_rate','explanation_coverage','minimality_ratio','verification_success_rate','context_tokens']].mean().reset_index(); summary.to_csv(f'{a.out}/ablation_summary.csv',index=False); summary.to_latex(f'{a.out}/tables/ablation_results.tex',index=False,float_format='%.3f'); print(summary)
