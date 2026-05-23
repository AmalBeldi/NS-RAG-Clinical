# NS-RAG Reproducible Prototype

Lightweight reproducible package for the NS-RAG experimental protocol.

It includes: synthetic de-identified EHR-like data, patient graph construction, graph summarization, RDF conversion, textual RAG, graph linearization, NS-RAG full, verification, minimal explanations, metrics, ablations, figures and LaTeX tables.

## Run
```bash
pip install -r requirements.txt
python src/run_experiment.py --input data/sample_ehr/patients.jsonl --out results
python src/run_ablation.py --input data/sample_ehr/patients.jsonl --out results
python src/make_figures.py --results results/summary_results.csv --ablation results/ablation_summary.csv --out results/figures
```

The included data are synthetic and intended only for reproducibility demonstration. Replace `patients.jsonl` with your preprocessed MIMIC-III/i2b2 instances using the same schema.