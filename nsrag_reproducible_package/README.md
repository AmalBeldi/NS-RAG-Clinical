# NS-RAG: Graph-Grounded Neuro-Symbolic RAG for Clinical QA

## Overview

NS-RAG is a graph-grounded neuro-symbolic framework for explainable and verifiable clinical question answering over EHR data.

The framework integrates:

- EHR graph construction
- graph summarization
- RDF grounding
- graph-based retrieval
- neuro-symbolic generation
- formal explainability
- graph-guided verification

## Repository Structure

data/               -> datasets
src/                -> pipeline source code
notebooks/          -> experiments and figures
results/            -> generated outputs
paper_snippets/     -> LaTeX tables and figures

## Installation

```bash
pip install -r requirements.txt
python src/run_experiment.py
python src/run_ablation.py
