def precision(pred,ref): return 0.0 if not pred else sum(1 for p in pred if p.lower() in [r.lower() for r in ref])/len(pred)
def recall(pred,ref): return 0.0 if not ref else sum(1 for r in ref if r.lower() in [p.lower() for p in pred])/len(ref)
def f1(p,r): return 0.0 if p+r==0 else 2*p*r/(p+r)
def hallucination_rate(pred,sup): return 0.0 if not pred else (len(pred)-len(sup))/len(pred)
def explanation_coverage(pred,sup): return 0.0 if not pred else len(sup)/len(pred)
def minimality_ratio(gmin,gexp): return 0.0 if gexp==0 else gmin/gexp
def verification_success(status): return 1.0 if status in {'OK','PARTIAL'} else 0.0
