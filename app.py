import streamlit as st
import json
from datetime import date

# ── Page config ──────────────────────────────────────
st.set_page_config(
    page_title="Force & Muscle",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap" rel="stylesheet">
<style>
:root {
  --black: #0a0a0a;
  --card: #1c1c1c;
  --border: #252525;
  --accent: #e8ff00;
  --accent2: #ff4d1c;
  --white: #f0ede6;
  --muted: #555;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background-color: #0a0a0a !important;
  color: #f0ede6 !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { background: #0a0a0a !important; }
[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

/* Hide default streamlit padding */
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 480px !important; }

/* Top bar */
.topbar {
  padding: 14px 0 12px;
  border-bottom: 1px solid #252525;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 0;
  position: relative;
}
.topbar::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(232,255,0,0.4), transparent);
}
.topbar-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 30px; line-height: 1; letter-spacing: 1px;
  color: #f0ede6;
}
.topbar-title span { color: #e8ff00; }
.topbar-meta {
  font-size: 9px; letter-spacing: 2px; text-transform: uppercase;
  color: #555; text-align: right; line-height: 1.7;
}

/* Tab buttons */
div[data-testid="stHorizontalBlock"] button {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  color: #555 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 9px !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  padding: 14px 8px !important;
  width: 100% !important;
  border-top: 2px solid transparent !important;
  transition: all 0.2s !important;
}
div[data-testid="stHorizontalBlock"] button:hover {
  color: #e8ff00 !important;
  border-top: 2px solid rgba(232,255,0,0.4) !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
  color: #e8ff00 !important;
  border-top: 2px solid #e8ff00 !important;
}

/* Week heading */
.week-heading {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 11px; letter-spacing: 4px; color: #555;
  text-transform: uppercase; margin-bottom: 12px; padding-top: 20px;
}

/* Day card */
.day-card {
  background: #1c1c1c;
  border: 1px solid #252525;
  border-radius: 14px;
  margin-bottom: 10px;
  overflow: hidden;
}
.day-card.rest { opacity: 0.55; }

.card-header {
  padding: 15px 16px;
  display: flex; align-items: center; gap: 13px;
}
.card-dot {
  width: 9px; height: 9px; border-radius: 50%;
  background: #e8ff00; flex-shrink: 0;
}
.card-dot.rest { background: #555; }
.card-info { flex: 1; min-width: 0; }
.card-day { font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #555; }
.card-name { font-family: 'Bebas Neue', sans-serif; font-size: 22px; line-height: 1.1; margin-top: 1px; color: #f0ede6; }
.card-muscles { font-size: 11px; color: #444; font-weight: 300; margin-top: 2px; }

/* Expanded detail */
.card-detail-inner {
  border-top: 1px solid #252525;
  padding: 14px 16px 18px;
}
.detail-warmup {
  font-size: 10px; color: #555; letter-spacing: 0.5px;
  margin-bottom: 14px;
}
.ex-row {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 11px 0;
  border-bottom: 1px solid #181818;
}
.ex-row:last-child { border-bottom: none; padding-bottom: 0; }
.ex-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 18px; color: #2a2a2a;
  width: 20px; flex-shrink: 0; text-align: right; margin-top: 1px;
}
.ex-info { flex: 1; }
.ex-name { font-size: 14px; font-weight: 500; color: #f0ede6; line-height: 1.3; }
.ex-note { font-size: 11px; color: #4a4a4a; font-weight: 300; margin-top: 3px; line-height: 1.4; }
.ex-chips { display: flex; gap: 5px; margin-top: 8px; flex-wrap: wrap; }
.chip {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 12px; letter-spacing: 0.5px;
  padding: 3px 8px; border-radius: 5px; display: inline-block;
}
.chip-sets { background: rgba(232,255,0,0.1); color: #e8ff00; }
.chip-reps { background: rgba(255,255,255,0.05); color: #888; }
.chip-rest { background: transparent; border: 1px solid #222; color: #444; font-family: 'DM Sans',sans-serif; font-size: 10px; letter-spacing: 0; }

/* Principes */
.stat-row {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;
  margin-bottom: 24px; margin-top: 8px;
}
.stat-card {
  background: #1c1c1c; border: 1px solid #252525;
  border-radius: 12px; padding: 14px 16px;
}
.stat-label { font-size: 8px; letter-spacing: 3px; text-transform: uppercase; color: #555; }
.stat-value { font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: #e8ff00; margin-top: 3px; line-height: 1; }

.section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 24px; letter-spacing: 1px;
  margin-bottom: 12px; margin-top: 24px;
  color: #f0ede6;
}

.principle-card {
  background: #1c1c1c; border: 1px solid #252525;
  border-radius: 12px; padding: 16px; margin-bottom: 8px;
  display: flex; gap: 13px; align-items: flex-start;
}
.principle-icon { font-size: 22px; flex-shrink: 0; margin-top: 1px; }
.principle-title { font-family: 'Bebas Neue', sans-serif; font-size: 17px; margin-bottom: 4px; color: #f0ede6; }
.principle-text { font-size: 12px; color: #666; font-weight: 300; line-height: 1.6; }

/* Tracker */
.tracker-section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 18px; letter-spacing: 1px; color: #e8ff00;
  margin-bottom: 8px; margin-top: 16px;
}

/* Form inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {
  background: #111 !important;
  border: 1px solid #252525 !important;
  color: #f0ede6 !important;
  border-radius: 7px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stDateInput input:focus {
  border-color: rgba(232,255,0,0.4) !important;
  box-shadow: none !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {
  color: #555 !important;
  font-size: 8px !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* Save button */
.stButton button[kind="primary"] {
  background: #e8ff00 !important;
  color: #0a0a0a !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 12px !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 15px !important;
  letter-spacing: 2px !important;
  width: 100% !important;
}
.stButton button {
  background: transparent !important;
  color: #555 !important;
  border: 1px solid #252525 !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* Log entries */
.log-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 12px; margin-top: 8px;
}
.log-count { font-size: 12px; color: #555; }
.log-count span { color: #e8ff00; font-family: 'Bebas Neue'; font-size: 16px; }

.log-entry {
  background: #1c1c1c; border: 1px solid #252525;
  border-radius: 10px; padding: 12px 14px;
  margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px;
}
.log-left { flex: 1; min-width: 0; }
.log-exercise { font-size: 13px; font-weight: 500; color: #f0ede6; }
.log-meta { font-size: 10px; color: #444; margin-top: 2px; }
.log-sets { font-size: 11px; color: #555; margin-top: 3px; font-family: 'Bebas Neue'; letter-spacing: 0.5px; }
.log-weight { font-family: 'Bebas Neue', sans-serif; font-size: 22px; color: #e8ff00; flex-shrink: 0; }
.log-weight small { font-size: 10px; color: #555; margin-left: 1px; font-family: 'DM Sans'; }

.empty-state {
  text-align: center; padding: 48px 20px;
  color: #333; font-size: 13px; line-height: 2;
}
.empty-icon { font-size: 40px; margin-bottom: 12px; }

/* Expander styling */
details summary {
  list-style: none;
}
[data-testid="stExpander"] {
  background: #1c1c1c !important;
  border: 1px solid #252525 !important;
  border-radius: 14px !important;
  margin-bottom: 10px !important;
}
[data-testid="stExpander"] summary {
  padding: 15px 16px !important;
  color: #f0ede6 !important;
}
[data-testid="stExpander"] summary p {
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 18px !important;
  color: #f0ede6 !important;
}
[data-testid="stExpander"] summary:hover {
  color: #e8ff00 !important;
}
[data-testid="stExpanderDetails"] {
  border-top: 1px solid #252525 !important;
  padding: 14px 16px 18px !important;
}
[data-testid="stExpanderToggleIcon"] { color: #e8ff00 !important; }

/* Dividers */
hr { border-color: #252525 !important; }

/* Success message */
.stSuccess { background: rgba(232,255,0,0.08) !important; border: 1px solid rgba(232,255,0,0.2) !important; color: #e8ff00 !important; border-radius: 8px !important; }

/* Tab bar bottom */
.tabbar-container {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: rgba(8,8,8,0.96);
  border-top: 1px solid #252525;
  height: 72px;
  display: flex;
  z-index: 1000;
}

/* Radio as tabs */
.stRadio [role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  gap: 0 !important;
}
.stRadio [role="radiogroup"] label {
  flex: 1;
  background: transparent !important;
  border: none !important;
  border-top: 2px solid transparent;
  border-radius: 0 !important;
  padding: 12px 8px !important;
  cursor: pointer;
  text-align: center;
  color: #555 !important;
  font-size: 9px !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  transition: all 0.2s !important;
}
.stRadio [role="radiogroup"] label:has(input:checked) {
  color: #e8ff00 !important;
  border-top: 2px solid #e8ff00 !important;
}
.stRadio input[type="radio"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────
PROGRAMME = [
    {
        "id": "j1",
        "day": "Jour 1 — Lundi",
        "name": "POUSSÉE",
        "muscles": "Pectoraux · Épaules · Triceps",
        "warmup": "Échauffement 10 min — mobilité épaules & coude",
        "exercises": [
            {"num": 1, "name": "Machine convergente à plat", "note": "Prise neutre — focus contraction pectorale, amplitude max", "sets": "4 séries", "reps": "6–8 rép", "rest": "3 min"},
            {"num": 2, "name": "Machine convergente inclinée", "note": "30–45° — faisceau claviculaire, contrôle excentrique", "sets": "4 séries", "reps": "8–10 rép", "rest": "2 min"},
            {"num": 3, "name": "Écarté cable basse poulie", "note": "Étirement maximal — meilleure hypertrophie pectorale", "sets": "3 séries", "reps": "12–15 rép", "rest": "90 sec"},
            {"num": 4, "name": "Développé militaire debout", "note": "Barre ou haltères — gainage abdominal strict", "sets": "4 séries", "reps": "6–8 rép", "rest": "2–3 min"},
            {"num": 5, "name": "Élévations latérales cable", "note": "Tension constante — 1 bras à la fois, éviter l'inertie", "sets": "3 séries", "reps": "12–15 rép", "rest": "90 sec"},
            {"num": 6, "name": "Dips lestés", "note": "Corps légèrement incliné — composé lourd triceps", "sets": "4 séries", "reps": "6–10 rép", "rest": "2 min"},
            {"num": 7, "name": "Seated overhead dips", "note": "Chef long en étirement maximal — amplitude profonde", "sets": "3 séries", "reps": "10–12 rép", "rest": "90 sec"},
            {"num": 8, "name": "Triceps poulie haute (corde)", "note": "Finition — supination en fin de course, contraction max", "sets": "3 séries", "reps": "12–15 rép", "rest": "60 sec"},
        ]
    },
    {
        "id": "j2",
        "day": "Jour 2 — Mardi",
        "name": "TIRAGE",
        "muscles": "Dos · Biceps · Trapèzes",
        "warmup": "Échauffement 10 min — mobilité épaules & thoracique",
        "exercises": [
            {"num": 1, "name": "Tirage vertical prise large", "note": "Largeur du dos — coudes vers les hanches, omoplate déprimée", "sets": "4 séries", "reps": "6–8 rép", "rest": "2–3 min"},
            {"num": 2, "name": "Tirage vertical prise serrée neutre", "note": "Étirement profond du grand dorsal — tirage vers le sternum", "sets": "4 séries", "reps": "8–10 rép", "rest": "2 min"},
            {"num": 3, "name": "Low Row Machine TechnoGym", "note": "Épaisseur dos & rhomboïdes — omoplates serrées en fin", "sets": "4 séries", "reps": "8–10 rép", "rest": "2 min"},
            {"num": 4, "name": "Face pull corde", "note": "Rotation externe — deltoïde post. & santé épaule", "sets": "3 séries", "reps": "15–20 rép", "rest": "90 sec"},
            {"num": 5, "name": "Curl barre EZ", "note": "Mouvement strict — ne pas balancer, tempo 2-0-1", "sets": "4 séries", "reps": "8–10 rép", "rest": "90 sec"},
            {"num": 6, "name": "Curl incliné haltères", "note": "Étirement long du biceps — banc 45–60°, supination en haut", "sets": "3 séries", "reps": "10–12 rép", "rest": "90 sec"},
            {"num": 7, "name": "Curl marteau haltères", "note": "Brachial & long supinateur — épaisseur du bras", "sets": "3 séries", "reps": "10–12 rép", "rest": "60 sec"},
        ]
    },
    {
        "id": "j3",
        "day": "Jour 3 — Mercredi",
        "name": "REPOS",
        "muscles": "Marche légère · Étirements · Récupération active",
        "rest": True,
    },
    {
        "id": "j4",
        "day": "Jour 4 — Jeudi",
        "name": "JAMBES",
        "muscles": "Quadriceps · Ischio-jambiers · Mollets",
        "warmup": "Échauffement 10 min — mobilité hanches & chevilles",
        "exercises": [
            {"num": 1, "name": "Squat barre haute", "note": "Mouvement roi — profondeur complète si mobilité OK", "sets": "5 séries", "reps": "4–6 rép", "rest": "3–4 min"},
            {"num": 2, "name": "Leg press 45°", "note": "Pieds hauts = ischio/fessiers · pieds bas = quadris", "sets": "4 séries", "reps": "10–12 rép", "rest": "2 min"},
            {"num": 3, "name": "Romanian Deadlift", "note": "Masse ischio — barre ou haltères, hanches en arrière", "sets": "4 séries", "reps": "8–10 rép", "rest": "2 min"},
            {"num": 4, "name": "Leg curl assis", "note": "Tension en étirement — supérieur au couché selon EMG récents", "sets": "3 séries", "reps": "10–12 rép", "rest": "90 sec"},
            {"num": 5, "name": "Leg curl couché", "note": "Bonne contraction en raccourcissement — angle complémentaire", "sets": "3 séries", "reps": "12–15 rép", "rest": "90 sec"},
            {"num": 6, "name": "Mollets debout machine", "note": "Amplitude complète — pause étirée en bas, contraction en haut", "sets": "4 séries", "reps": "12–15 rép", "rest": "60 sec"},
        ]
    },
    {
        "id": "j5",
        "day": "Jour 5 — Vendredi",
        "name": "FULL BODY",
        "muscles": "Force composés — charges maximales",
        "warmup": "Séance force pure — rester à 1–2 reps du failure sur chaque set",
        "exercises": [
            {"num": 1, "name": "Soulevé de terre classique", "note": "Mouvement principal — charge maximale contrôlée", "sets": "5 séries", "reps": "2–4 rép", "rest": "4–5 min"},
            {"num": 2, "name": "Machine convergente à plat", "note": "Charge lourde — tempo lent, intention maximale", "sets": "4 séries", "reps": "6–8 rép", "rest": "3 min"},
            {"num": 3, "name": "Tractions lestées", "note": "Prise large pronation — dos large", "sets": "4 séries", "reps": "5–6 rép", "rest": "3 min"},
            {"num": 4, "name": "Développé militaire barre", "note": "Debout — gainage abdominal strict", "sets": "4 séries", "reps": "5–6 rép", "rest": "2–3 min"},
            {"num": 5, "name": "Ab wheel / Planche RKC", "note": "Gainage anti-extension — core fonctionnel", "sets": "3 séries", "reps": "8–10 / 30s", "rest": "60 sec"},
        ]
    },
    {
        "id": "j67",
        "day": "Jours 6 & 7 — Week-end",
        "name": "REPOS",
        "muscles": "Activité libre · Sommeil · Nutrition prioritaires",
        "rest": True,
    },
]

PRINCIPES = {
    "entrainement": [
        {"icon": "📈", "title": "Surcharge Progressive", "text": "Augmentez la charge de 2,5–5 kg dès que vous réalisez toutes les séries dans la fourchette haute de répétitions."},
        {"icon": "🎯", "title": "Intensité Contrôlée", "text": "Restez à 1–2 répétitions du failure sur les composés. L'échec est réservé aux exercices d'isolation."},
        {"icon": "⏱", "title": "Tempo & Technique", "text": "Phase excentrique lente (2–3 sec). Jamais de sacrifice technique pour ajouter du poids."},
        {"icon": "🔄", "title": "Décharge (Deload)", "text": "Toutes les 4–6 semaines, réduisez le volume de 40–50% pour permettre une super-compensation."},
    ],
    "nutrition": [
        {"icon": "🍽", "title": "Protéines", "text": "Visez 1,8–2,2 g / kg de poids corporel. Léger surplus calorique de 200–300 kcal pour la prise de masse."},
        {"icon": "💤", "title": "Sommeil", "text": "7–9h de sommeil sont non-négociables. La croissance musculaire se produit au repos, pas en salle."},
        {"icon": "💧", "title": "Hydratation", "text": "2–3 L d'eau/jour minimum. La déshydratation réduit la force de 5–10%. Davantage les jours d'entraînement."},
    ]
}

# ── Session state ────────────────────────────────────
if "tab" not in st.session_state:
    st.session_state.tab = "🗓 Programme"
if "gym_log" not in st.session_state:
    st.session_state.gym_log = []
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# ── Top Bar ──────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-title">FORCE <span>&</span> MUSCLE</div>
  <div class="topbar-meta">PPL + FB<br>4 JOURS / SEM</div>
</div>
""", unsafe_allow_html=True)

# ── Tab Navigation ───────────────────────────────────
tab_labels = ["🗓 Programme", "⚡ Principes", "📋 Suivi"]
st.markdown('<div style="background: rgba(8,8,8,0.96); border-bottom: 1px solid #252525; margin-bottom: 20px;">', unsafe_allow_html=True)
selected_tab = st.radio("", tab_labels, horizontal=True, label_visibility="collapsed", key="tab_radio")
st.markdown('</div>', unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────
def render_exercise(ex):
    return f"""
<div class="ex-row">
  <div class="ex-num">{ex['num']}</div>
  <div class="ex-info">
    <div class="ex-name">{ex['name']}</div>
    <div class="ex-note">{ex['note']}</div>
    <div class="ex-chips">
      <span class="chip chip-sets">{ex['sets']}</span>
      <span class="chip chip-reps">{ex['reps']}</span>
      <span class="chip chip-rest">{ex['rest']}</span>
    </div>
  </div>
</div>"""

# ── PROGRAMME TAB ────────────────────────────────────
if selected_tab == "🗓 Programme":
    st.markdown('<div class="week-heading">— Semaine type —</div>', unsafe_allow_html=True)

    for day in PROGRAMME:
        if day.get("rest"):
            st.markdown(f"""
<div class="day-card rest">
  <div class="card-header">
    <div class="card-dot rest"></div>
    <div class="card-info">
      <div class="card-day">{day['day']}</div>
      <div class="card-name">{day['name']}</div>
      <div class="card-muscles">{day['muscles']}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
        else:
            label = f"{day['day']} · {day['name']} · {day['muscles']}"
            with st.expander(f"**{day['name']}** — {day['day'].split('—')[0].strip()}"):
                exs_html = f'<div class="card-detail-inner"><div class="detail-warmup">🔥 {day["warmup"]}</div>'
                for ex in day["exercises"]:
                    exs_html += render_exercise(ex)
                exs_html += "</div>"
                st.markdown(exs_html, unsafe_allow_html=True)

# ── PRINCIPES TAB ────────────────────────────────────
elif selected_tab == "⚡ Principes":
    st.markdown("""
<div class="stat-row">
  <div class="stat-card"><div class="stat-label">Fréquence</div><div class="stat-value">4J/SEM</div></div>
  <div class="stat-card"><div class="stat-label">Durée séance</div><div class="stat-value">60–75M</div></div>
  <div class="stat-card"><div class="stat-label">Méthode</div><div class="stat-value">PPL+FB</div></div>
  <div class="stat-card"><div class="stat-label">Niveau</div><div class="stat-value">INTER+</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Entraînement</div>', unsafe_allow_html=True)
    for p in PRINCIPES["entrainement"]:
        st.markdown(f"""
<div class="principle-card">
  <div class="principle-icon">{p['icon']}</div>
  <div>
    <div class="principle-title">{p['title']}</div>
    <div class="principle-text">{p['text']}</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Nutrition & Récupération</div>', unsafe_allow_html=True)
    for p in PRINCIPES["nutrition"]:
        st.markdown(f"""
<div class="principle-card">
  <div class="principle-icon">{p['icon']}</div>
  <div>
    <div class="principle-title">{p['title']}</div>
    <div class="principle-text">{p['text']}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── TRACKER TAB ──────────────────────────────────────
elif selected_tab == "📋 Suivi":
    st.markdown('<div class="tracker-section-title">+ Nouvelle séance</div>', unsafe_allow_html=True)

    # Session → exercise mapping
    SESSION_EXERCISES = {
        "Jour 1 — Poussée": [ex["name"] for ex in next(d for d in PROGRAMME if d["id"] == "j1")["exercises"]],
        "Jour 2 — Tirage":  [ex["name"] for ex in next(d for d in PROGRAMME if d["id"] == "j2")["exercises"]],
        "Jour 4 — Jambes":  [ex["name"] for ex in next(d for d in PROGRAMME if d["id"] == "j4")["exercises"]],
        "Jour 5 — Full Body": [ex["name"] for ex in next(d for d in PROGRAMME if d["id"] == "j5")["exercises"]],
    }

    # Track selected session outside the form to dynamically update exercise list
    if "selected_session" not in st.session_state:
        st.session_state.selected_session = ""

    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            t_date = st.date_input("Date", value=date.today())
        with col2:
            session_options = ["", "Jour 1 — Poussée", "Jour 2 — Tirage", "Jour 4 — Jambes", "Jour 5 — Full Body"]
            t_session = st.selectbox("Séance", session_options)

        # Dynamic exercise dropdown
        if t_session and t_session in SESSION_EXERCISES:
            exercise_options = ["Choisir un exercice..."] + SESSION_EXERCISES[t_session] + ["Autre (saisir manuellement)"]
            t_exercise_select = st.selectbox("Exercice", exercise_options)
            if t_exercise_select == "Autre (saisir manuellement)":
                t_exercise = st.text_input("Exercice (manuel)", placeholder="Ex: Curl concentration")
            elif t_exercise_select == "Choisir un exercice...":
                t_exercise = ""
            else:
                t_exercise = t_exercise_select
                st.markdown(f'<div style="font-size:11px;color:#444;margin-top:-8px;margin-bottom:8px;padding-left:2px;">✓ Sélectionné</div>', unsafe_allow_html=True)
        else:
            t_exercise = st.text_input("Exercice", placeholder="Choisissez d'abord une séance...")

        col3, col4 = st.columns(2)
        with col3:
            t_weight = st.number_input("Charge (kg)", min_value=0.0, step=2.5, format="%.1f")
        with col4:
            t_sets = st.text_input("Séries × Reps", placeholder="Ex: 4×8")

        t_notes = st.text_input("Notes", placeholder="Ressenti, technique...")

        submitted = st.form_submit_button("ENREGISTRER", type="primary")

        if submitted and t_exercise.strip():
            entry = {
                "id": len(st.session_state.gym_log),
                "date": t_date.strftime("%d/%m/%Y"),
                "session": t_session,
                "exercise": t_exercise.strip(),
                "weight": t_weight if t_weight > 0 else None,
                "sets": t_sets,
                "notes": t_notes,
            }
            st.session_state.gym_log.insert(0, entry)
            st.session_state.gym_log = st.session_state.gym_log[:100]
            st.session_state.show_success = True
            st.rerun()
        elif submitted:
            st.warning("⚠ Veuillez renseigner l'exercice.")

    if st.session_state.show_success:
        st.success("✓ Séance enregistrée !")
        st.session_state.show_success = False

    # Log display
    st.markdown("<br>", unsafe_allow_html=True)
    log = st.session_state.gym_log

    if not log:
        st.markdown("""
<div class="empty-state">
  <div class="empty-icon">🏋️</div>
  Aucune séance enregistrée.<br>Commencez à tracker vos performances !
</div>""", unsafe_allow_html=True)
    else:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown(f'<div class="log-count">Historique <span>{len(log)}</span></div>', unsafe_allow_html=True)
        with col_h2:
            if st.button("🗑 Tout vider"):
                st.session_state.gym_log = []
                st.rerun()

        to_delete = None
        for i, e in enumerate(log):
            col_e, col_d = st.columns([6, 1])
            with col_e:
                weight_html = f'<div class="log-weight">{e["weight"]}<small>kg</small></div>' if e.get("weight") else ""
                sets_html = f'<div class="log-sets">{e["sets"]}</div>' if e.get("sets") else ""
                notes_html = f'<div class="log-meta" style="font-style:italic;margin-top:2px">{e["notes"]}</div>' if e.get("notes") else ""
                meta = e["date"]
                if e.get("session"):
                    meta += f" · {e['session']}"
                st.markdown(f"""
<div class="log-entry">
  <div class="log-left">
    <div class="log-exercise">{e['exercise']}</div>
    <div class="log-meta">{meta}</div>
    {sets_html}
    {notes_html}
  </div>
  {weight_html}
</div>""", unsafe_allow_html=True)
            with col_d:
                if st.button("✕", key=f"del_{i}"):
                    to_delete = i

        if to_delete is not None:
            st.session_state.gym_log.pop(to_delete)
            st.rerun()
