import streamlit as st
import ollama
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import re
import imaplib
import email
import pandas as pd
from email.header import decode_header
from bs4 import BeautifulSoup
import io


# Connexion à Ollama avec DeepSeek
OLLAMA_API_BASE = "http://ollama:11434"
MODEL_NAME = "deepseek-r1"

llm = ChatOllama(base_url=OLLAMA_API_BASE, model=MODEL_NAME)

# Configuration IMAP
EMAIL_ACCOUNT = "yassircheikh5@gmail.com"
EMAIL_PASSWORD = "osgv wfqx nymi rpho"
IMAP_SERVER = "imap.gmail.com"  # Pour Gmail, sinon adaptez

def clean_email_content(msg):
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
    return content.strip()

def get_last_n_emails(n=10):
    emails = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()[-n:]  # Les N derniers emails

        for email_id in reversed(email_ids):
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    sender = msg["From"]
                    content = clean_email_content(msg)
                    emails.append((sender, subject, content))
        mail.logout()
    except Exception as e:
        st.error(f"Erreur de récupération des emails : {str(e)}")
    return emails

# Interface Streamlit
st.set_page_config(page_title="Détecteur de Spam", page_icon="📧", layout="centered")


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
st.markdown("## 📧 Détecteur de Spam avec DeepSeek")
# Récupération du dernier email
if st.button("📥 Lancer l’analyse des 10 derniers emails"):
    email_list = get_last_n_emails(10)

    if not email_list:
        st.warning("Aucun email trouvé.")
    else:
        result_data = []

        for idx, (sender, subject, content) in enumerate(email_list, 1):
            with st.expander(f"📧 Email #{idx} - {subject}"):
                st.write(f"**Expéditeur :** {sender}")
                st.text_area("✉️ Contenu :", content, height=150, disabled=True)

                with st.spinner("Analyse en cours..."):
                    try:
                        prompt = f"""
                        Voici un email reçu :
                        Expéditeur : {sender}
                        Objet : {subject}
                        Contenu : {content}

                        Analyse cet email et donne un score de probabilité de spam entre 0 et 100.
                        Réponds uniquement sous la forme : 'Spam Score: X' où X est un nombre entier.
                        Voici des exemples :

                        Email 1 :
                        Expéditeur : contact@lotteries-winner.com
                        Objet : Félicitations ! Vous avez gagné 1 000 000 € !
                        Contenu : Cliquez ici pour réclamer votre prix. Ne ratez pas cette chance unique !
                        Spam Score: 95

                        Email 2 :
                        Expéditeur : hr@entreprise.com
                        Objet : Entretien prévu demain
                        Contenu : Bonjour, je vous confirme notre entretien prévu demain à 14h.
                        Spam Score: 5

                        Email 3 :
                        Expéditeur : promo@ventes-flash.biz
                        Objet : -70% sur tous les produits aujourd'hui seulement !!!
                        Contenu : Achetez maintenant et profitez d'offres exceptionnelles.
                        Spam Score: 88

                        Email 4 :
                        Expéditeur : support@banque.fr
                        Objet : Alerte de sécurité
                        Contenu : Veuillez vérifier vos informations de connexion via notre site sécurisé.
                        Spam Score: 35

                        """
                        response = llm([HumanMessage(content=prompt)])
                        spam_result = response.content.strip()

                        match = re.search(r'Spam Score: (\d+)', spam_result)
                        if match:
                            score = int(match.group(1))
                            label = "SPAM" if score >= 50 else "NON SPAM"

                            st.write(f"📊 **Score détecté : {score}/100**")
                            if label == "SPAM":
                                st.error("🚨 SPAM détecté !")
                            else:
                                st.success("✅ Non SPAM.")

                            result_data.append({
                                "Expéditeur": sender,
                                "Objet": subject,
                                "Contenu": content,
                                "Score": score,
                                "Label": label
                            })
                        else:
                            st.warning("⚠️ Score non détecté.")
                    except Exception as e:
                        st.error(f"Erreur LLM : {str(e)}")

        # Création et téléchargement du CSV
        if result_data:
            df = pd.DataFrame(result_data)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.success("✅ Analyse terminée ! Téléchargez les résultats :")
            st.download_button(
                label="📥 Télécharger les résultats CSV",
                data=csv_data,
                file_name="resultats_emails_spam.csv",
                mime="text/csv"
            )