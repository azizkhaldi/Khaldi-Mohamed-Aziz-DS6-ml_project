# Utiliser une image Python légère
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY api.py .
COPY model.pkl .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Lancer l’API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
