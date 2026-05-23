class DeterministicClinicalGenerator:
    def generate(self,prompt):
        p=prompt.lower()
        if 'glycemic' in p or 'hba1c' in p: return 'Worsening glycemic control is suggested by elevated HbA1c and glucose values.'
        if 'anemia' in p or 'hemoglobin' in p: return 'Anemia is supported by low hemoglobin and reduced iron-related markers.'
        if 'renal' in p or 'kidney' in p or 'creatinine' in p or 'egfr' in p: return 'Impaired renal function is suggested by elevated creatinine and reduced eGFR.'
        if 'medication' in p:
            meds=[m for m in ['Metformin','Insulin glargine','Amlodipine','Lisinopril','Oral iron','Erythropoietin','Furosemide'] if m.lower() in p]
            return 'The documented medications include '+(', '.join(meds[:4]) if meds else 'current treatments recorded in the patient file')+'.'
        return 'The patient summary includes diagnoses, medications, laboratory findings, and recent clinical events.'
def build_prompt(task,question,context): return f"Task: {task}\nQuestion: {question}\nContext:\n{context}\nAnswer:"
