import streamlit as st

st.set_page_config(page_title="NS-RAG Demo", layout="wide")

st.title("NS-RAG: Graph-Grounded Neuro-Symbolic Clinical AI")

st.markdown("""
Prototype demonstrator for explainable and verifiable clinical question answering
based on knowledge graphs, RAG, symbolic verification, and minimal explanations.
""")

# Sidebar
st.sidebar.title("Configuration")

patient_id = st.sidebar.selectbox(
    "Select patient",
    ["Patient P001", "Patient P002", "Patient P003"]
)

task = st.sidebar.selectbox(
    "Clinical task",
    [
        "Clinical Summarization",
        "Disease Progression",
        "Temporal Explanation"
    ]
)

question = st.sidebar.text_input(
    "Clinical question",
    "What evidence suggests disease progression?"
)

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Graph Nodes", "42")
col2.metric("RDF Triples", "118")
col3.metric("Confidence", "0.91")
col4.metric("Verification", "OK")

# Pipeline
st.subheader("1. NS-RAG Pipeline")

st.graphviz_chart("""
digraph {
    rankdir=LR;
    node [shape=box, style=rounded];

    EHR -> GraphSynth;
    GraphSynth -> DGsumm;
    DGsumm -> RDFGraphSyn;
    RDFGraphSyn -> Retrieval;
    Retrieval -> LLM;
    LLM -> Verification;
    Verification -> Explanation;
}
""")

# Patient EHR
st.subheader("2. Patient EHR Snapshot")

st.table({
    "Clinical Feature": [
        "Age",
        "Diagnosis",
        "IGHV status",
        "Lymphocytes",
        "Temporal motif",
        "Treatment status"
    ],
    "Value": [
        "67",
        "Chronic Lymphocytic Leukemia",
        "Mutated",
        "45 G/L",
        "Rapid lymphocyte increase",
        "No treatment yet"
    ]
})

# Knowledge Graph
st.subheader("3. Patient-Centric Knowledge Graph")

st.graphviz_chart("""
digraph {
    rankdir=LR;

    Patient [shape=ellipse, style=filled, fillcolor=lightblue];
    CLL [shape=box];
    Lymphocytosis [shape=box];
    RapidIncrease [shape=box];
    IGHV_Mutated [shape=box];
    ProgressiveCLL [shape=box, style=filled, fillcolor=lightcoral];

    Patient -> CLL [label="hasDiagnosis"];
    Patient -> Lymphocytosis [label="hasBiomarker"];
    Lymphocytosis -> RapidIncrease [label="hasTemporalMotif"];
    Patient -> IGHV_Mutated [label="hasGeneticMarker"];
    RapidIncrease -> ProgressiveCLL [label="supports"];
}
""")

# Graph summary
st.subheader("4. Task-Oriented Graph Summary")

st.info("""
DGsumm selects the clinically relevant subgraph for the selected task:
temporal biomarker evolution, discriminant motifs, and progression-related evidence.
""")

# Retrieved evidence
st.subheader("5. Retrieved Graph Evidence")

st.code("""
(Patient_P001, hasDiagnosis, CLL)
(Patient_P001, hasBiomarker, Lymphocytosis)
(Lymphocytosis, hasTemporalMotif, RapidIncrease)
(RapidIncrease, supports, ProgressiveCLL)
""")

# Generated answer
st.subheader("6. Generated Clinical Answer")

st.success("""
The patient shows evidence of possible disease progression. This is mainly supported
by progressive lymphocytosis and a rapid temporal increase motif. The generated answer
is grounded in the patient-centered RDF graph and verified against structured evidence.
""")

# Verification
st.subheader("7. Neuro-Symbolic Verification")

st.table({
    "Generated Claim": [
        "The patient has CLL",
        "Lymphocytosis is present",
        "A rapid increase motif is detected",
        "The case supports progressive evolution"
    ],
    "Verification Status": [
        "VERIFIED",
        "VERIFIED",
        "VERIFIED",
        "SUPPORTED"
    ],
    "Evidence Source": [
        "Diagnosis node",
        "Biomarker node",
        "Temporal motif node",
        "Explanation path"
    ]
})

# Minimal explanation graph
st.subheader("8. Minimal Explanation Graph")

st.graphviz_chart("""
digraph {
    rankdir=LR;

    Lymphocytosis [shape=box, style=filled, fillcolor=lightyellow];
    RapidIncrease [shape=box, style=filled, fillcolor=lightyellow];
    ProgressiveCLL [shape=box, style=filled, fillcolor=lightcoral];

    Lymphocytosis -> RapidIncrease [label="temporal motif"];
    RapidIncrease -> ProgressiveCLL [label="supports"];
}
""")

# Final interpretation
st.subheader("9. Interpretation")

st.markdown("""
The minimal explanation graph shows that the final answer does not rely on the
entire patient graph. Instead, NS-RAG extracts a compact evidence subgraph
connecting biomarker evolution, temporal motifs, and progression-oriented reasoning.
""")