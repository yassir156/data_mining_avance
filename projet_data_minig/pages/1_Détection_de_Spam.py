import streamlit as st
import ollama
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import re  # Pour extraire le score de spam

# Connexion à Ollama avec DeepSeek
OLLAMA_API_BASE = "http://ollama:11434"
MODEL_NAME = "deepseek-r1"

llm = ChatOllama(base_url=OLLAMA_API_BASE, model=MODEL_NAME)

# Configuration de la page avec un design moderne
st.set_page_config(page_title="Détecteur de Spam", page_icon="📧", layout="centered")

# CSS personnalisé pour améliorer le design
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

        /* Animation du fond */
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
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

        /* Style du titre */
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

        /* Zone de texte avec effet */
        .stTextArea textarea {
            background-color: #393552 !important;
            color: white !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            border: 1px solid #eb6f92 !important;
            padding: 10px !important;
            transition: all 0.3s ease-in-out;
        }

        /* Effet au focus */
        .stTextArea textarea:focus {
            border: 1px solid #9ccfd8 !important;
            box-shadow: 0px 0px 10px rgba(156, 207, 216, 0.5);
        }

        /* Bouton stylisé */
        .stButton > button {
            background: linear-gradient(135deg, #31748f, #3e8e9e);
            color: white;
            border-radius: 15px;
            font-size: 20px;
            padding: 12px 28px;
            border: none;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        /* Effet au survol */
        .stButton > button:hover {
            background: linear-gradient(135deg, #286983, #265a7e);
            transform: scale(1.08);
            box-shadow: 6px 6px 20px rgba(0, 0, 0, 0.6);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Icône animée
st.markdown('<p class="email-icon">📧</p>', unsafe_allow_html=True)

# Titre principal avec animation
st.markdown("<p class='title'>🔍 Détecteur de Spam avec DeepSeek</p>", unsafe_allow_html=True)

# Message de bienvenue
st.write("Bienvenue ! Entrez un email pour analyser s'il est un spam.")

# Zone de texte stylisée
email_content = st.text_area("✉️ Collez votre email ici :", height=200)

# Bouton animé
if st.button("🚀 Analyser"):
    if email_content:
        try:
            # Génération de la réponse
            prompt = f"""
            Analyse cet email et donne un score de probabilité de spam entre 0 et 100.
            Réponds uniquement sous la forme : 'Spam Score: X' où X est un nombre entier.
            
            Email : {email_content}
            """
            response = llm([HumanMessage(content=prompt)])
            spam_result = response.content.strip()

            # Extraction du score avec regex
            match = re.search(r'Spam Score: (\d+)', spam_result)
            if match:
                score = int(match.group(1))  # Convertir en entier
                st.write(f"📊 **Score détecté : {score}/100**")

                # Définition du seuil
                if score >= 50:
                    st.error("🚨 Cet email est considéré comme un SPAM !")
                else:
                    st.success("✅ Cet email est considéré comme NON SPAM.")
            else:
                st.warning("⚠️ Impossible d'extraire le score. Vérifiez la réponse du modèle.")

        except Exception as e:
            st.error(f"Erreur de connexion à Ollama : {str(e)}")
    else:
        st.warning("⚠️ Veuillez entrer un email à analyser.")



import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

# Configuration IMAP
EMAIL_ACCOUNT = "yassircheikh5@gmail.com"
EMAIL_PASSWORD = ""
IMAP_SERVER = "imap.gmail.com"  # Pour Gmail, sinon adaptez

def get_last_email():
    try:
        # Connexion au serveur IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")  # Sélection de la boîte de réception

        # Récupération du dernier email
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        if not email_ids:
            return None

        latest_email_id = email_ids[-1]  # Dernier email
        _, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                sender = msg["From"]

                # Extraction du contenu de l'email
                content = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                        elif content_type == "text/html":
                            html_content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            soup = BeautifulSoup(html_content, "html.parser")
                            content = soup.get_text()
                            break
                else:
                    content = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                mail.logout()
                return sender, subject, content.strip()

    except Exception as e:
        print(f"Erreur lors de la récupération des emails : {e}")
        return None

# Exemple d'utilisation
sender, subject, content = get_last_email()
print("Expéditeur :", sender)
print("Objet :", subject)
print("Contenu :", content[:500])  # Affiche un extrait du mail
