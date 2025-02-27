# Utiliser l'image officielle Python (basée sur Debian)
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer les paquets
COPY requirements.txt .
RUN python3 -m pip config set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
