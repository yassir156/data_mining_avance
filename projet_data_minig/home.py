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
            font-size: 42px;
            font-weight: bold;
            color: #eb6f92;
            animation: fadeIn 1.5s ease-in-out;
        }

        /* Animation du titre */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Style de la description au-dessus des boutons */
        .button-description {
            font-size: 18px;
            color: #c4a7e7;
            margin-bottom: 10px;
            animation: fadeIn 1.8s ease-in-out;
        }

        /* Conteneur pour centrer les boutons */
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
            border-radius: 15px;
            font-size: 20px;
            padding: 14px 28px;
            border: none;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        /* Effet au survol des boutons */
        .stButton > button:hover {
            background: linear-gradient(135deg, #286983, #265a7e);
            transform: scale(1.08);
            box-shadow: 6px 6px 20px rgba(0, 0, 0, 0.6);
        }

        /* Icône animée */
        .email-icon {
            font-size: 60px;
            animation: bounce 1.5s infinite;
        }

        /* Animation de l'icône */
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Icône d'email animée
st.markdown('<p class="email-icon">📧</p>', unsafe_allow_html=True)

# Titre principal
st.markdown("<p class='title'>🔍 Analyse des Emails avec Ollama</p>", unsafe_allow_html=True)

# Description
st.write("Bienvenue sur l'application d'analyse des emails. Choisissez une option ci-dessous 👇")

# Conteneur des boutons avec descriptions
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='button-description'>📩 Vérifiez si un email est un **spam** grâce à une IA avancée.</p>", unsafe_allow_html=True)
    if st.button("📧 Détection de Spam"):
        st.switch_page("pages/1_Détection_de_Spam.py")

with col2:
    st.markdown("<p class='button-description'>📊 Découvrez les **tendances et patterns** des emails en quelques clics.</p>", unsafe_allow_html=True)
    if st.button("📊 Analyse des Tendances"):
        st.switch_page("pages/2_Analyse_des_Tendances.py")
