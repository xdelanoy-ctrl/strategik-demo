
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stratégik - Démo", page_icon="🎯")

st.title("🎯 Stratégik – Démo IA de reconversion (version semi-adaptative)")
st.markdown("Réponds à ces 10 questions. À la fin, Stratégik t’indiquera les métiers les plus compatibles avec ton profil.")

questions = [
    {"text": "Aimes-tu être au contact de la nature ?", "mot_cle": "nature"},
    {"text": "Te sens-tu à l’aise pour aider les autres ?", "mot_cle": "aide"},
    {"text": "Préféres-tu travailler seul ou en équipe ?", "mot_cle": "autonomie"},
    {"text": "Souhaites-tu éviter les environnements stressants ?", "mot_cle": "stress"},
    {"text": "Es-tu attiré par le travail manuel ou créatif ?", "mot_cle": "créatif"},
    {"text": "Veux-tu éviter de travailler dans un laboratoire ?", "mot_cle": "laboratoire"},
    {"text": "As-tu envie d’un métier avec un impact social fort ?", "mot_cle": "social"},
    {"text": "Préféres-tu un travail en extérieur ?", "mot_cle": "extérieur"},
    {"text": "Souhaites-tu éviter la hiérarchie très marquée ?", "mot_cle": "hiérarchie"},
    {"text": "As-tu envie d’un métier lié au numérique ?", "mot_cle": "numérique"},
]

ponderation = {
    "Appétence forte": 40,
    "Appétence modérée": 25,
    "Tolérance": 10,
    "Rejet modéré": -40,
    "Rejet catégorique": -100
}

user_answers = []

for idx, q in enumerate(questions):
    answer = st.selectbox(
        f"{idx+1}. {q['text']}",
        list(ponderation.keys()),
        key=f"q{idx}"
    )
    user_answers.append({
        "mot_cle": q["mot_cle"],
        "intensite": answer,
        "score": ponderation[answer]
    })

# Base métier simplifiée
df_rome = pd.DataFrame([
    {"code_rome": "K1201", "intitule": "Intervention sociale", "competences": "aide, social, médiation"},
    {"code_rome": "M1805", "intitule": "Direction de projet numérique", "competences": "gestion, numérique, stress"},
    {"code_rome": "A1203", "intitule": "Maraîchage", "competences": "nature, extérieur, manuel"},
    {"code_rome": "D1209", "intitule": "Recherche en biologie", "competences": "laboratoire, analyse"},
    {"code_rome": "G1804", "intitule": "Pâtissier", "competences": "créatif, manuel"},
])

def calculer_score(metier, reponses):
    score = 0
    for rep in reponses:
        if rep["mot_cle"] in metier["competences"]:
            score += rep["score"]
    return score

if st.button("Voir les métiers compatibles"):
    df_rome["score"] = df_rome.apply(lambda row: calculer_score(row, user_answers), axis=1)
    df_sorted = df_rome[df_rome["score"] > -100].sort_values(by="score", ascending=False)

    st.subheader("🔎 Résultats de compatibilité métier :")
    for _, row in df_sorted.iterrows():
        st.markdown(f"**{row['intitule']}** – Code ROME : `{row['code_rome']}`  
Score : {row['score']}")

    # Détection red flag
    for rep in user_answers:
        if rep["score"] <= -100:
            st.error("⚠️ Un rejet catégorique a été détecté. Nous te recommandons d’en parler avec ton formateur.")
            break
