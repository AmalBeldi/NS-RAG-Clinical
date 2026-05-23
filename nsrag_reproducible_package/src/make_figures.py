import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
def save(out,name): plt.tight_layout(); plt.savefig(Path(out)/f'{name}.pdf',bbox_inches='tight'); plt.savefig(Path(out)/f'{name}.png',dpi=300,bbox_inches='tight'); plt.close()
p=argparse.ArgumentParser(); p.add_argument('--results',required=True); p.add_argument('--ablation',required=True); p.add_argument('--out',default='results/figures'); a=p.parse_args(); Path(a.out).mkdir(parents=True,exist_ok=True)
df=pd.read_csv(a.results); qa=df[df.task=='qa']
plt.figure(figsize=(6,4)); plt.bar(qa.method,qa.hallucination_rate); plt.ylabel('Hallucination Rate ↓'); plt.xticks(rotation=30,ha='right'); plt.title('Hallucination Rate by Method'); save(a.out,'hallucination_by_method')
plt.figure(figsize=(6,4)); plt.scatter(qa.explanation_coverage,qa.fact_f1,s=120); [plt.annotate(r.method,(r.explanation_coverage,r.fact_f1),xytext=(4,4),textcoords='offset points') for _,r in qa.iterrows()]; plt.xlabel('Explanation Coverage ↑'); plt.ylabel('Fact F1 ↑'); plt.title('Accuracy vs Explainability'); save(a.out,'accuracy_vs_explainability')
abl=pd.read_csv(a.ablation); plt.figure(figsize=(7,4)); plt.plot(abl.method,abl.fact_f1,marker='o',label='Fact F1'); plt.plot(abl.method,1-abl.hallucination_rate,marker='o',label='1-HR'); plt.plot(abl.method,abl.explanation_coverage,marker='o',label='EC'); plt.ylabel('Score'); plt.xticks(rotation=30,ha='right'); plt.title('Ablation Study'); plt.legend(); save(a.out,'ablation_study')
