import streamlit as st

# Configuration de la page principale
st.set_page_config(page_title="Analyse des Emails", page_icon="📧", layout="centered")

# CSS personnalisé pour améliorer le design avec des animations et un effet premium
st.markdown(
    """
    <style>
        /* Fond avec animation en dégradé */
        .stApp {
            background: linear-gradient(-45deg, #1f1d2e, #26233a, #3a3d5c, #171720);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite;
            color: white !important;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }

        /* Animation de l'arrière-plan */
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Style du titre avec animation */
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #eb6f92;
            animation: fadeIn 1.5s ease-in-out;
            text-shadow: 4px 4px 10px rgba(255, 255, 255, 0.2);
        }

        /* Animation du titre */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Style de la description */
        .description {
            font-size: 20px;
            color: #c4a7e7;
            margin-bottom: 20px;
            animation: fadeIn 1.8s ease-in-out;
        }

        /* Conteneur des boutons */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
        }

        /* Style des boutons */
        .stButton > button {
            background: linear-gradient(135deg, #31748f, #3e8e9e);
            color: white;
            border-radius: 20px;
            font-size: 22px;
            padding: 16px 32px;
            border: none;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        /* Effet au survol des boutons */
        .stButton > button:hover {
            background: linear-gradient(135deg, #286983, #265a7e);
            transform: scale(1.1);
            box-shadow: 6px 6px 20px rgba(0, 0, 0, 0.6);
        }

        /* Icône animée */
        .email-icon {
            font-size: 70px;
            animation: bounce 1.5s infinite;
            color: #c4a7e7;
            text-shadow: 3px 3px 10px rgba(255, 255, 255, 0.3);
        }

        /* Animation de l'icône */
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        /* Effet flip pour la section d'informations */
        .info-box {
            perspective: 1000px;
            width: 320px;
            height: 150px;
            margin: 30px auto;
        }

        .info-inner {
            width: 100%;
            height: 100%;
            position: relative;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }

        .info-box:hover .info-inner {
            transform: rotateY(180deg);
        }

        .info-front, .info-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.2);
        }

        .info-front {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 20px;
        }

        .info-back {
            background-color: rgba(235, 111, 146, 0.9);
            color: white;
            font-size: 18px;
            transform: rotateY(180deg);
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Icône d'email animée
st.markdown('<p class="email-icon">📧</p>', unsafe_allow_html=True)

# Titre principal
st.markdown("<p class='title'>🔍 Analyse des Emails avec Ollama</p>", unsafe_allow_html=True)

# Description améliorée
st.markdown("<p class='description'>Bienvenue sur l'application d'analyse des emails. Découvrez si un email est un spam ou analysez ses tendances en un clic !</p>", unsafe_allow_html=True)

# Conteneur des boutons avec descriptions
col1, col2 = st.columns(2)

with col1:
    if st.button("📧 Détection de Spam"):
        st.switch_page("pages/1_Détection_de_Spam.py")

with col2:
    if st.button("📊 Analyse des Tendances"):
        st.switch_page("pages/2_Analyse_des_Tendances.py")

# Section d'informations avec effet flip
st.markdown("""
    <div class='info-box'>
        <div class='info-inner'>
            <div class='info-front'>🔎 Infos utiles</div>
            <div class='info-back'>Savez-vous que plus de 45% des emails envoyés dans le monde sont du spam ? Utilisez notre outil pour rester protégé !</div>
        </div>
    </div>
""", unsafe_allow_html=True)
