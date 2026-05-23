import re
def extract_assertions(text): return [x.strip() for x in re.split(r'[.;\n]+',text) if x.strip()]
def support_terms(record):
    terms=[]
    for x in record.get('diagnoses',[]): terms += [x.lower()] + [t for t in x.lower().split() if len(t)>4]
    for x in record.get('medications',[]): terms.append(x.lower())
    for l in record.get('labs',[]): terms += [str(l.get('name','')).lower(), str(l.get('value','')).lower()]
    return set(t for t in terms if t)
def verify_assertions(assertions,record):
    terms=support_terms(record); sup=[]; uns=[]
    for a in assertions: (sup if any(t in a.lower() for t in terms) else uns).append(a)
    return sup,uns
def verification_status(score,theta_ok=0.8,theta_partial=0.4): return 'OK' if score>=theta_ok else ('PARTIAL' if score>=theta_partial else 'KO')
