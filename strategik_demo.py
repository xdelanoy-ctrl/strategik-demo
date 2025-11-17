
import pandas as pd
from typing import List, Dict

# Simuler un mini-extrait d'un fichier ROME
data = [
    {"code_rome": "K1201", "intitule": "Intervention sociale", "competences": "écoute, aide, médiation, empathie"},
    {"code_rome": "M1805", "intitule": "Direction de projet", "competences": "gestion, stress, planification"},
    {"code_rome": "A1203", "intitule": "Maraîchage", "competences": "nature, travail physique, autonomie"},
    {"code_rome": "D1209", "intitule": "Recherche en biologie", "competences": "laboratoire, analyse, expérimentation"}
]
df_rome = pd.DataFrame(data)

# Simuler des réponses utilisateur avec intensité
user_responses = [
    {"text": "Je suis passionné par la nature", "type": "appétence forte", "mot_cle": "nature"},
    {"text": "Je ne veux plus jamais travailler en laboratoire", "type": "rejet catégorique", "mot_cle": "laboratoire"},
    {"text": "Je suis plutôt à l’aise pour aider les autres", "type": "appétence modérée", "mot_cle": "aide"},
    {"text": "Je préfère éviter les métiers trop stressants", "type": "rejet modéré", "mot_cle": "stress"}
]

# Pondération par type d'intensité
ponderation = {
    "appétence forte": 40,
    "appétence modérée": 25,
    "tolérance": 10,
    "rejet modéré": -40,
    "rejet catégorique": -100
}

# Calcul des scores
def calculer_score_metier(metier: Dict, reponses: List[Dict]) -> int:
    score = 0
    for rep in reponses:
        if rep["mot_cle"] in metier["competences"]:
            score += ponderation[rep["type"]]
    return score

# Appliquer les scores
df_rome["score"] = df_rome.apply(lambda row: calculer_score_metier(row, user_responses), axis=1)

# Trier les métiers par score décroissant, ignorer les -100
df_resultats = df_rome[df_rome["score"] > -100].sort_values(by="score", ascending=False).reset_index(drop=True)

# Afficher les résultats
print(df_resultats[["code_rome", "intitule", "score"]])
