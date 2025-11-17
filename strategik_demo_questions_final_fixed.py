
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stratégik – Reconversion", layout="centered")

# Données ROME fictives
data = [
    {"code_rome": "K1201", "intitule": "Intervention sociale", "competences": "écoute, aide, médiation, empathie"},
    {"code_rome": "M1805", "intitule": "Direction de projet", "competences": "gestion, stress, planification"},
    {"code_rome": "A1203", "intitule": "Maraîchage", "competences": "nature, travail physique, autonomie"},
    {"code_rome": "D1209", "intitule": "Recherche en biologie", "competences": "laboratoire, analyse, expérimentation"},
    {"code_rome": "G1804", "intitule": "Pâtisserie", "competences": "créativité, autonomie, rigueur"},
]
df_rome = pd.DataFrame(data)

# Questionnaire
questions = [
    {"question": "Avez-vous un attrait fort pour le travail en extérieur ou proche de la nature ?", "mot_cle": "nature"},
    {"question": "Vous sentez-vous à l’aise pour accompagner ou aider des personnes en difficulté ?", "mot_cle": "aide"},
    {"question": "Préférez-vous travailler de manière autonome sans supervision constante ?", "mot_cle": "autonomie"},
    {"question": "Êtes-vous attiré par la gestion de projets et la planification d’activités complexes ?", "mot_cle": "planification"},
    {"question": "Ressentez-vous du stress en situation de gestion ou de coordination d’équipe ?", "mot_cle": "stress"},
    {"question": "Souhaiteriez-vous éviter tout travail en laboratoire ?", "mot_cle": "laboratoire"},
    {"question": "Vous considérez-vous comme quelqu’un de créatif dans votre approche du travail ?", "mot_cle": "créativité"},
    {"question": "Appréciez-vous les tâches impliquant de la rigueur et de la précision ?", "mot_cle": "rigueur"},
    {"question": "Avez-vous de l’intérêt pour les environnements liés à la recherche ou à la science ?", "mot_cle": "analyse"},
    {"question": "Souhaitez-vous éviter le contact direct avec le public ou les bénéficiaires ?", "mot_cle": "écoute"},
]

ponderation = {
    "Appétence forte": 40,
    "Appétence modérée": 25,
    "Tolérance neutre": 10,
    "Rejet modéré": -40,
    "Rejet catégorique": -100
}

# Interface utilisateur
st.title("🎯 Stratégik – Assistant de Reconversion Professionnelle")

prenom = st.text_input("Quel est ton prénom suivi de la première lettre de ton nom ? (ex : Sophie M.)")

if prenom:
    st.success(f"Bienvenue {prenom}. Merci de répondre aux 10 questions ci-dessous.")

    if "responses" not in st.session_state:
        st.session_state.responses = {}

    for idx, q in enumerate(questions):
        st.session_state.responses[q["mot_cle"]] = st.selectbox(
            f"{idx+1}. {q['question']}",
            list(ponderation.keys()),
            key=f"q{idx}"
        )

    if st.button("Analyser les réponses et proposer des métiers"):
        user_responses = []
        red_flags = []

        for mot_cle, choix in st.session_state.responses.items():
            user_responses.append({
                "mot_cle": mot_cle,
                "type": choix
            })
            if ponderation[choix] <= -100:
                red_flags.append(mot_cle)

        def calculer_score(row):
            score = 0
            for rep in user_responses:
                if rep["mot_cle"] in row["competences"]:
                    score += ponderation[rep["type"]]
            return score

        df_rome["score"] = df_rome.apply(calculer_score, axis=1)
        df_sorted = df_rome[df_rome["score"] > -100].sort_values(by="score", ascending=False)

        st.subheader("🧠 Métiers compatibles selon vos préférences :")
        for _, row in df_sorted.iterrows():
            st.markdown(
                f"**{row['intitule']}** – Code ROME : `{row['code_rome']}`  
"
                f"Score : {row['score']}"
            )

        if red_flags:
            st.warning("⚠️ Une ou plusieurs réponses indiquent un rejet fort ou une souffrance possible. Merci d’en parler avec votre formateur.")
