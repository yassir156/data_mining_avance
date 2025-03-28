import streamlit as st
import pandas as pd
import time
import random
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage

# Connexion à Ollama
OLLAMA_API_BASE = "http://ollama:11434"
MODEL_NAME = "deepseek-r1"
llm = ChatOllama(base_url=OLLAMA_API_BASE, model=MODEL_NAME)

# Configuration de la page principale
st.set_page_config(page_title="📊 Analyse des Tendances", page_icon="📧", layout="centered")

# CSS personnalisé pour le design moderne et animé
st.markdown(
    """
    <style>
        /* Fond animé */
        .stApp {
            background: linear-gradient(-45deg, #1f1d2e, #26233a, #3a3d5c, #171720);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite;
            color: white !important;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Titre animé */
        .title {
            font-size: 42px;
            font-weight: bold;
            color: #9ccfd8;
            animation: fadeIn 1.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Conteneur pour centrer les boutons */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
        }

        /* Style des boutons */
        .stButton > button {
            background: linear-gradient(135deg, #31748f, #3e8e9e);
            color: white;
            border-radius: 10px;
            font-size: 20px;
            padding: 12px 24px;
            border: none;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #286983, #265a7e);
            transform: scale(1.05);
            box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5);
        }

        /* Animation de chargement */
        @keyframes loadingDots {
            0% { content: "."; }
            33% { content: ".."; }
            66% { content: "..."; }
            100% { content: "."; }
        }

        .loading-text::after {
            content: ".";
            animation: loadingDots 1.5s infinite;
        }

        /* Style de la carte de résultats */
        .result-box {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
            text-align: left;
            font-size: 18px;
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal animé
st.markdown("<p class='title'>📊 Analyse des Tendances dans les Emails</p>", unsafe_allow_html=True)
st.write("💡 Charge un dataset d'emails et découvre les tendances cachées dans leur contenu.")

# Zone de chargement de fichier
uploaded_file = st.file_uploader("📂 Charge un fichier CSV contenant des emails", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("🔍 **Aperçu des données chargées :**")
    st.dataframe(df.head())

    if st.button("🚀 Analyser les Tendances"):
        with st.spinner("🔍 Analyse en cours..."):
            try:
                # 1. Préparation du contenu pour le LLM
                max_rows = min(15, len(df))
                selected_rows = df.sample(n=max_rows, random_state=random.randint(1, 100))

                # Construction du prompt avec contexte structuré
                rows_text = ""
                for i, row in selected_rows.iterrows():
                    rows_text += f"""
                        Email {i+1} :
                        Expéditeur : {row['Expéditeur']}
                        Objet : {row['Objet']}
                        Score : {row['Score']}
                        Label : {row['Label']}
                        Contenu : {row['Contenu']}
                        ---
                        """

                final_prompt = f"""
                Tu es un expert en analyse de contenu email. On t'a donné une liste d'emails classés avec un score de spam et des libellés.

                Voici un extrait d'exemples :

                {rows_text}

                Analyse les tendances générales dans ces emails :
                - Quels sont les mots ou sujets récurrents ?
                - Y a-t-il des motifs communs dans les SPAM ?
                - Quels types d'expéditeurs semblent suspects ?
                - Fais un petit résumé analytique clair, utile, et structuré.

                Réponds sous forme d'un **rapport clair**.
                """

                response = llm([HumanMessage(content=final_prompt)])
                trends = response.content.strip()

                # Affichage stylisé du rapport
                st.markdown("<h3 style='color: #eb6f92;'>📈 Rapport d'Analyse des Tendances :</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-box'> {trends} </div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Erreur lors de l'analyse : {str(e)}")
