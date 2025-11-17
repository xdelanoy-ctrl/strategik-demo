import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stratégik – Reconversion", layout="centered")

# -------------------------------------------------------------------
# Données ROME fictives
# -------------------------------------------------------------------

data = [
    {
        "code_rome": "K1201",
        "intitule": "Intervention sociale",
        "competences": "écoute, aide, médiation, empathie",
    },
    {
        "code_rome": "M1403",
        "intitule": "Direction de projet",
        "competences": "gestion, stress, planification",
    },
    {
        "code_rome": "A1405",
        "intitule": "Maraîchage",
        "competences": "nature, travail physique, autonomie",
    },
    {
        "code_rome": "H1206",
        "intitule": "Recherche en biologie",
        "competences": "laboratoire, analyse, expérimentation",
    },
    {
        "code_rome": "D1102",
        "intitule": "Pâtisserie",
        "competences": "créativité, autonomie, rigueur",
    },
]

df_rome = pd.DataFrame(data)

# -------------------------------------------------------------------
# Questionnaire
# -------------------------------------------------------------------

questions = [
    {
        "question": "Avez-vous un attrait fort pour le travail en extérieur ou proche de la nature ?",
        "mot_cle": "nature",
    },
    {
        "question": "Vous sentez-vous à l’aise pour accompagner ou aider des personnes en difficulté ?",
        "mot_cle": "aide",
    },
    {
        "question": "Préférez-vous travailler de manière autonome sans supervision constante ?",
        "mot_cle": "autonomie",
    },
    {
        "question": "Êtes-vous attiré par la gestion de projets et la planification d’activités complexes ?",
        "mot_cle": "planification",
    },
    {
        "question": "Ressentez-vous du stress en situation de gestion ou de coordination d’équipe ?",
        "mot_cle": "stress",
    },
    {
        "question": "Souhaiteriez-vous éviter tout travail en laboratoire ?",
        "mot_cle": "laboratoire",
    },
    {
        "question": "Vous aimez créer quelque chose de concret à partir de vos mains (artisanat, cuisine, etc.) ?",
        "mot_cle": "créativité",
    },
    {
        "question": "Appréciez-vous les tâches impliquant de la rigueur et de la précision ?",
        "mot_cle": "rigueur",
    },
    {
        "question": "Êtes-vous à l’aise avec les environnements liés à la recherche ou à la science ?",
        "mot_cle": "analyse",
    },
    {
        "question": "Souhaitez-vous éviter le contact direct avec le public ou les bénéficiaires ?",
        "mot_cle": "écoute",
    },
]

ponderation = {
    "Appétence forte": 40,
    "Appétence modérée": 20,
    "Tolérance neutre": 10,
    "Rejet modéré": -40,
    "Rejet catégorique": -100,
}

# Mot-clés considérés comme sensibles pour les "red flags"
mot_cles_sensibles = {"stress", "souffrance", "épuisement"}

# -------------------------------------------------------------------
# Initialisation de l'état
# -------------------------------------------------------------------

if "responses" not in st.session_state:
    st.session_state.responses = []

st.title("Stratégik – Démo de questionnaire métiers")

st.write(
    "Ce module propose quelques questions simples pour dégager de grandes tendances "
    "et voir quels métiers ROME fictifs semblent les plus compatibles avec vos préférences."
)

# -------------------------------------------------------------------
# Formulaire de réponses
# -------------------------------------------------------------------

with st.form("questionnaire"):
    st.subheader("Vos réponses")

    responses_local = []
    red_flags = []

    choix_possibles = list(ponderation.keys())

    for q in questions:
        rep = st.radio(
            q["question"],
            options=choix_possibles,
            index=2,  # par défaut : Tolérance neutre
            key=f"q_{q['mot_cle']}",
        )
        responses_local.append({"mot_cle": q["mot_cle"], "type": rep})

        # Signaux d’alerte : rejet fort sur certains thèmes sensibles
        if rep in ("Rejet modéré", "Rejet catégorique") and q["mot_cle"] in mot_cles_sensibles:
            red_flags.append(q["mot_cle"])

    submitted = st.form_submit_button("Analyser mes réponses")

# Mise à jour de l'état si formulaire soumis
if submitted:
    st.session_state.responses = responses_local
    st.session_state.red_flags = red_flags
else:
    red_flags = st.session_state.get("red_flags", [])

# -------------------------------------------------------------------
# Calcul du score et tri des métiers
# -------------------------------------------------------------------

def calculer_score(row: pd.Series) -> int:
    """Calcule le score d'un métier en fonction des réponses utilisateur."""
    score = 0
    for rep in st.session_state.responses:
        mot_cle = rep["mot_cle"]
        reponse = rep["type"]
        if mot_cle in row.get("competences", ""):
            score += ponderation.get(reponse, 0)
    return score


if st.session_state.responses:
    df_scored = df_rome.assign(score=df_rome.apply(calculer_score, axis=1))
    df_sorted = (
        df_scored[df_scored["score"] > -100]
        .sort_values(by="score", ascending=False)
        .reset_index(drop=True)
    )

    # -------------------------------------------------------------------
    # Affichage des résultats
    # -------------------------------------------------------------------

    st.subheader("🔎 Métiers compatibles selon vos préférences")

    if df_sorted.empty:
        st.info(
            "Aucun métier compatible trouvé avec les préférences actuelles. "
            "Vous pouvez essayer de modifier certaines réponses."
        )
    else:
        # Top 3 affiché proprement
        top_n = min(3, len(df_sorted))
        st.write(f"Voici les {top_n} métiers qui ressortent le plus dans cet échantillon :")

        for rank, (_, row) in enumerate(df_sorted.head(top_n).iterrows(), start=1):
            st.markdown(
                f"""### {rank}. {row['intitule']}
Code ROME : `{row['code_rome']}`  
Score global : **{row['score']}**"""
            )

            if row["score"] >= 80:
                st.caption("➡ Profil très compatible dans cette petite démo.")
            elif row["score"] >= 40:
                st.caption("➡ Piste intéressante à explorer plus en détail.")
            else:
                st.caption("➡ Compatibilité faible mais à discuter selon le contexte.")

            st.markdown("---")

    # -------------------------------------------------------------------
    # Alerte en cas de signaux rouges
    # -------------------------------------------------------------------

    if red_flags:
        st.warning(
            "⚠️ Une ou plusieurs réponses indiquent un rejet fort ou une souffrance "
            "possible. Merci d’en parler avec votre formateur."
        )
else:
    st.info(
        "Répondez aux questions ci-dessus puis cliquez sur « Analyser mes réponses » "
        "pour voir les résultats."
    )
