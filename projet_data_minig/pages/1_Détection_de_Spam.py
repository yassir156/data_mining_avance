import streamlit as st
import ollama
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import re  # Pour extraire le score de spam
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

# Connexion à Ollama avec DeepSeek
OLLAMA_API_BASE = "http://ollama:11434"
MODEL_NAME = "deepseek-r1"

llm = ChatOllama(base_url=OLLAMA_API_BASE, model=MODEL_NAME)

# Configuration IMAP
EMAIL_ACCOUNT = "yassircheikh5@gmail.com"
EMAIL_PASSWORD = ""
IMAP_SERVER = "imap.gmail.com"  # Pour Gmail, sinon adaptez

def get_last_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

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
        return None

# Interface Streamlit
st.set_page_config(page_title="Détecteur de Spam", page_icon="📧", layout="centered")

st.markdown("## 📧 Détecteur de Spam avec DeepSeek")

# Récupération du dernier email
email_data = get_last_email()

if email_data:
    sender, subject, email_content = email_data
    st.write(f"**Expéditeur :** {sender}")
    st.write(f"**Objet :** {subject}")
    st.text_area("✉️ Contenu de l'email :", email_content, height=200, disabled=True)
    
    if st.button("🚀 Analyser"):
        try:
            prompt = f"""
            Voici un email reçu :
            
            Expéditeur : {sender}
            Objet : {subject}
            Contenu : {email_content}
            
            Analyse cet email et donne un score de probabilité de spam entre 0 et 100.
            Réponds uniquement sous la forme : 'Spam Score: X' où X est un nombre entier.
            """
            response = llm([HumanMessage(content=prompt)])
            spam_result = response.content.strip()

            match = re.search(r'Spam Score: (\d+)', spam_result)
            if match:
                score = int(match.group(1))
                st.write(f"📊 **Score détecté : {score}/100**")
                
                if score >= 50:
                    st.error("🚨 Cet email est considéré comme un SPAM !")
                else:
                    st.success("✅ Cet email est considéré comme NON SPAM.")
            else:
                st.warning("⚠️ Impossible d'extraire le score. Vérifiez la réponse du modèle.")
        except Exception as e:
            st.error(f"Erreur de connexion à Ollama : {str(e)}")
else:
    st.warning("⚠️ Aucun email récupéré. Veuillez vérifier votre connexion IMAP.")
