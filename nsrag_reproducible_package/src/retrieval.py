from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def split_chunks(notes):
    out=[]
    for note in notes: out.extend([x.strip() for x in note.replace(';','.').split('.') if x.strip()])
    return out

def textual_rag_context(record, question, top_k=3):
    chunks=split_chunks(record.get('notes',[]))
    if not chunks: return ''
    vec=TfidfVectorizer().fit_transform(chunks+[question]); sims=cosine_similarity(vec[-1],vec[:-1]).flatten(); idx=np.argsort(-sims)[:top_k]
    return '\n'.join(chunks[i] for i in idx)
def graph_context(text,max_tokens=2048): return ' '.join(text.split()[:max_tokens])
