# 💪 Force & Muscle — Streamlit App

Programme de musculation PPL + Full Body · 4 jours/semaine · Niveau intermédiaire+

## 🚀 Déploiement rapide sur Streamlit Cloud

1. **Fork / clone** ce repo sur ton GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io)
3. Connecte ton GitHub et sélectionne ce repo
4. **Main file path** : `app.py`
5. Clique **Deploy** → c'est en ligne en 2 minutes !

## 📦 Structure

```
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
├── .streamlit/
│   └── config.toml    # Thème sombre personnalisé
└── README.md
```

## 🏃 Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✨ Fonctionnalités

- **Programme** : 4 séances détaillées (Poussée · Tirage · Jambes · Full Body)
- **Principes** : Surcharge progressive, nutrition, récupération
- **Suivi** : Tracker de séances avec historique (session state)
