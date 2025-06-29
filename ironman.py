import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="Préparation Ironman 70.3",
    page_icon="🏊‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #4ECDC4;
    }
    
    .workout-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
    }
    
    .nutrition-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #45B7D1;
        margin: 0.5rem 0;
        color: #333333;
    }
    
    .completed {
        opacity: 0.6;
        text-decoration: line-through;
    }
</style>
""", unsafe_allow_html=True)

# Données du programme d'entraînement
TRAINING_PROGRAM = {
    1: {  # Semaine 1
        'Lundi': {
            'natation': '1 heure, technique et endurance',
            'course': '30 minutes facile',
            'nutrition': 'Petit-déjeuner riche en glucides (flocons d\'avoine avec fruits). Collation post-entraînement avec des protéines (yaourt grec avec miel).'
        },
        'Mardi': {
            'velo': '1 heure 30 minutes, endurance à intensité modérée',
            'nutrition': 'Déjeuner équilibré avec poulet grillé, quinoa et légumes. Hydratation constante pendant l\'entraînement.'
        },
        'Mercredi': {
            'natation': '45 minutes, intervalles (10 x 100 mètres nage rapide)',
            'course': '45 minutes, fractionné (5 x 400 mètres course)',
            'nutrition': 'Smoothie protéiné post-entraînement. Dîner avec saumon, patate douce et épinards pour les oméga-3 et les vitamines.'
        },
        'Jeudi': {
            'velo': '2 heures, avec montées pour travailler la force',
            'nutrition': 'En-cas énergétiques pendant le vélo (barres de céréales, bananes). Dîner avec pâtes complètes et sauce tomate pour les glucides.'
        },
        'Vendredi': {
            'natation': '1 heure, endurance en nage continue',
            'course': '30 minutes facile',
            'nutrition': 'Déjeuner léger avec salade de lentilles et légumes. Collation avec des noix et fruits secs.'
        },
        'Samedi': {
            'velo': '3 heures, endurance',
            'course': '20 minutes facile en transition vélo-course',
            'nutrition': 'Petit-déjeuner consistant avec pancakes et sirop d\'érable. Hydratation avec boissons isotoniques pendant l\'entraînement.'
        },
        'Dimanche': {
            'course': '1 heure facile pour récupération active',
            'nutrition': 'Repas de récupération avec omelette aux légumes et avocat. Hydratation accrue pour la récupération.'
        }
    },
    2: {  # Semaine 2
        'Lundi': {
            'natation': '1 heure, technique',
            'course': '40 minutes à rythme modéré',
            'nutrition': 'Petit-déjeuner avec toast de pain complet et beurre de cacahuète. Collation post-entraînement avec fromage blanc et fruits rouges.'
        },
        'Mardi': {
            'velo': '2 heures, endurance avec intervalles (5 x 3 minutes à haute intensité)',
            'nutrition': 'Déjeuner avec bœuf maigre, riz brun et brocoli. Boire beaucoup d\'eau pour rester hydraté.'
        },
        'Mercredi': {
            'natation': '50 minutes, intervalles (8 x 200 mètres nage rapide)',
            'course': '50 minutes, fractionné (6 x 800 mètres course)',
            'nutrition': 'Smoothie vert post-entraînement avec épinards, banane et protéine en poudre. Dîner avec poulet rôti et légumes variés.'
        },
        'Jeudi': {
            'velo': '2 heures 30 minutes, avec montées pour travailler la force et l\'endurance',
            'nutrition': 'En-cas avec des fruits secs et des amandes pendant le vélo. Dîner avec poisson blanc et quinoa.'
        },
        'Vendredi': {
            'natation': '1 heure, endurance en nage continue',
            'course': '35 minutes facile',
            'nutrition': 'Déjeuner avec wrap de dinde et légumes. Collation avec un mélange de noix et graines.'
        },
        'Samedi': {
            'velo': '3 heures 30 minutes, endurance',
            'course': '25 minutes facile en transition vélo-course',
            'nutrition': 'Petit-déjeuner avec muesli et lait d\'amande. Boissons énergétiques pendant l\'entraînement.'
        },
        'Dimanche': {
            'course': '1 heure 15 minutes facile pour récupération active',
            'nutrition': 'Repas de récupération avec tofu grillé et légumes sautés. Hydratation avec eau de coco pour les électrolytes.'
        }
    },
    3: {  # Semaine 3
        'Lundi': {
            'natation': '1 heure, technique et endurance',
            'course': '45 minutes à rythme modéré',
            'nutrition': 'Petit-déjeuner avec granola et yaourt. Collation post-entraînement avec barres protéinées.'
        },
        'Mardi': {
            'velo': '2 heures, endurance avec intervalles (6 x 4 minutes à haute intensité)',
            'nutrition': 'Déjeuner avec saumon, pâtes complètes et asperges. Hydratation avec boissons isotoniques.'
        },
        'Mercredi': {
            'natation': '55 minutes, intervalles (6 x 300 mètres nage rapide)',
            'course': '55 minutes, fractionné (4 x 1 kilomètre course)',
            'nutrition': 'Smoothie post-entraînement avec mangue et protéine en poudre. Dîner avec dinde, purée de patate douce et haricots verts.'
        },
        'Jeudi': {
            'velo': '3 heures, avec montées pour travailler la force et l\'endurance',
            'nutrition': 'En-cas avec des fruits frais et des noix pendant le vélo. Dîner avec soupe de légumes et pain complet.'
        },
        'Vendredi': {
            'natation': '1 heure, endurance en nage continue',
            'course': '40 minutes facile',
            'nutrition': 'Déjeuner avec salade de poulet et avocat. Collation avec des fruits et fromage cottage.'
        },
        'Samedi': {
            'velo': '4 heures, endurance',
            'course': '30 minutes facile en transition vélo-course, simulation de course',
            'nutrition': 'Petit-déjeuner avec crêpes et fruits frais. Hydratation et nutrition constante pendant l\'entraînement.'
        },
        'Dimanche': {
            'course': '1 heure facile pour récupération active',
            'nutrition': 'Repas de récupération avec œufs brouillés et légumes grillés. Hydratation avec eau et électrolytes.'
        }
    }
}

# Conseils nutritionnels généraux
NUTRITION_TIPS = [
    "🥤 Bois au moins 2,5 à 3 litres d'eau par jour",
    "🍎 Équilibre glucides, protéines et graisses saines à chaque repas",
    "🥗 Privilégie les aliments complets et non transformés",
    "🍌 Prends une collation riche en glucides 30-60 min avant l'entraînement",
    "🥛 Consomme des protéines dans les 30 min après l'entraînement",
    "🥑 Intègre des oméga-3 (poisson, noix, graines de lin)",
    "🍯 Utilise des sucres naturels pour l'énergie (miel, fruits)",
    "🥕 Mange varié pour couvrir tous les besoins en vitamines"
]

# Fonctions utilitaires
def save_data(data, filename):
    """Sauvegarde les données dans un fichier JSON"""
    with open(filename, 'w') as f:
        json.dump(data, f, default=str)

def load_data(filename):
    """Charge les données depuis un fichier JSON"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def get_current_week():
    """Calcule la semaine actuelle du programme"""
    start_date = date(2025, 6, 29)  # Date de début
    current_date = date.today()
    days_diff = (current_date - start_date).days
    week = min((days_diff // 7) + 1, 3)  # Maximum 3 semaines dans le programme
    return max(1, week)

def get_current_day():
    """Retourne le jour actuel en français"""
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    return days[date.today().weekday()]

# Initialisation des données de session
if 'completed_workouts' not in st.session_state:
    st.session_state.completed_workouts = load_data('completed_workouts.json')

if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = load_data('sleep_data.json')

if 'nutrition_log' not in st.session_state:
    st.session_state.nutrition_log = load_data('nutrition_log.json')

# En-tête principal
st.markdown('<div class="main-header">🏊‍♂️ Préparation Ironman 70.3 🚴‍♂️🏃‍♂️</div>', unsafe_allow_html=True)

# Calcul des statistiques
race_date = date(2025, 8, 24)
days_remaining = (race_date - date.today()).days
current_week = get_current_week()
current_day = get_current_day()

# Affichage des statistiques
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{days_remaining}</div>
        <div>Jours restants</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_workouts = sum(len([k for k in day.keys() if k != 'nutrition']) 
                        for week in TRAINING_PROGRAM.values() 
                        for day in week.values())
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_workouts}</div>
        <div>Entraînements totaux</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    completed_count = len(st.session_state.completed_workouts)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{completed_count}</div>
        <div>Entraînements faits</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">S{current_week}</div>
        <div>Semaine actuelle</div>
    </div>
    """, unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3, tab4 = st.tabs(["📅 Programme du jour", "💪 Entraînements", "🍽️ Nutrition", "😴 Sommeil"])

with tab1:
    st.header(f"Programme du {current_day} - Semaine {current_week}")
    
    if current_week <= 3 and current_day in TRAINING_PROGRAM[current_week]:
        day_program = TRAINING_PROGRAM[current_week][current_day]
        
        # Entraînements du jour
        st.subheader("🏋️‍♂️ Entraînements")
        for activity, description in day_program.items():
            if activity != 'nutrition':
                workout_key = f"{current_week}_{current_day}_{activity}"
                is_completed = workout_key in st.session_state.completed_workouts
                
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    completed = st.checkbox("", key=f"check_{workout_key}", value=is_completed)
                    if completed and workout_key not in st.session_state.completed_workouts:
                        st.session_state.completed_workouts[workout_key] = str(datetime.now())
                        save_data(st.session_state.completed_workouts, 'completed_workouts.json')
                    elif not completed and workout_key in st.session_state.completed_workouts:
                        del st.session_state.completed_workouts[workout_key]
                        save_data(st.session_state.completed_workouts, 'completed_workouts.json')
                
                with col2:
                    emoji = {"natation": "🏊‍♂️", "velo": "🚴‍♂️", "course": "🏃‍♂️"}
                    class_name = "workout-card completed" if is_completed else "workout-card"
                    st.markdown(f"""
                    <div class="{class_name}">
                        <strong>{emoji.get(activity, "💪")} {activity.title()}</strong><br>
                        {description}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Conseils nutrition du jour
        if 'nutrition' in day_program:
            st.subheader("🥗 Conseils nutrition")
            st.markdown(f"""
            <div class="nutrition-card">
                {day_program['nutrition']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun entraînement programmé pour aujourd'hui ou programme terminé.")

with tab2:
    st.header("💪 Vue d'ensemble des entraînements")
    
    week_filter = st.selectbox("Choisir la semaine", [1, 2, 3], index=current_week-1)
    
    for day, program in TRAINING_PROGRAM[week_filter].items():
        st.subheader(f"{day} - Semaine {week_filter}")
        
        for activity, description in program.items():
            if activity != 'nutrition':
                workout_key = f"{week_filter}_{day}_{activity}"
                is_completed = workout_key in st.session_state.completed_workouts
                
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    completed = st.checkbox("", key=f"overview_{workout_key}", value=is_completed)
                    if completed and workout_key not in st.session_state.completed_workouts:
                        st.session_state.completed_workouts[workout_key] = str(datetime.now())
                        save_data(st.session_state.completed_workouts, 'completed_workouts.json')
                    elif not completed and workout_key in st.session_state.completed_workouts:
                        del st.session_state.completed_workouts[workout_key]
                        save_data(st.session_state.completed_workouts, 'completed_workouts.json')
                
                with col2:
                    emoji = {"natation": "🏊‍♂️", "velo": "🚴‍♂️", "course": "🏃‍♂️"}
                    class_name = "workout-card completed" if is_completed else "workout-card"
                    st.markdown(f"""
                    <div class="{class_name}">
                        <strong>{emoji.get(activity, "💪")} {activity.title()}</strong><br>
                        {description}
                    </div>
                    """, unsafe_allow_html=True)

with tab3:
    st.header("🍽️ Nutrition et conseils")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Log quotidien")
        today_str = str(date.today())
        
        # Repas du jour
        breakfast = st.text_area("Petit-déjeuner", 
                                value=st.session_state.nutrition_log.get(f"{today_str}_breakfast", ""),
                                key="breakfast")
        lunch = st.text_area("Déjeuner", 
                            value=st.session_state.nutrition_log.get(f"{today_str}_lunch", ""),
                            key="lunch")
        dinner = st.text_area("Dîner", 
                             value=st.session_state.nutrition_log.get(f"{today_str}_dinner", ""),
                             key="dinner")
        snacks = st.text_area("Collations", 
                             value=st.session_state.nutrition_log.get(f"{today_str}_snacks", ""),
                             key="snacks")
        
        if st.button("💾 Sauvegarder nutrition"):
            st.session_state.nutrition_log[f"{today_str}_breakfast"] = breakfast
            st.session_state.nutrition_log[f"{today_str}_lunch"] = lunch
            st.session_state.nutrition_log[f"{today_str}_dinner"] = dinner
            st.session_state.nutrition_log[f"{today_str}_snacks"] = snacks
            save_data(st.session_state.nutrition_log, 'nutrition_log.json')
            st.success("Nutrition sauvegardée !")
    
    with col2:
        st.subheader("💡 Conseils nutrition")
        for tip in NUTRITION_TIPS:
            st.markdown(f"• {tip}")
        
        st.subheader("🎯 Objectifs hydratation")
        water_intake = st.number_input("Eau consommée aujourd'hui (litres)", 
                                      value=st.session_state.nutrition_log.get(f"{today_str}_water", 0.0),
                                      min_value=0.0, max_value=10.0, step=0.1)
        
        if st.button("💧 Sauvegarder hydratation"):
            st.session_state.nutrition_log[f"{today_str}_water"] = water_intake
            save_data(st.session_state.nutrition_log, 'nutrition_log.json')
            st.success("Hydratation sauvegardée !")
        
        # Indicateur visuel hydratation
        progress = min(water_intake / 3.0, 1.0)
        st.progress(progress)
        if water_intake >= 3.0:
            st.success("🎉 Objectif hydratation atteint !")
        else:
            remaining = 3.0 - water_intake
            st.info(f"Il vous reste {remaining:.1f}L à boire")

with tab4:
    st.header("😴 Suivi du sommeil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌙 Sommeil d'hier")
        yesterday = str(date.today() - timedelta(days=1))
        
        sleep_time = st.time_input("Heure de coucher", 
                                  value=datetime.strptime(st.session_state.sleep_data.get(f"{yesterday}_bedtime", "22:00"), "%H:%M").time())
        wake_time = st.time_input("Heure de réveil", 
                                 value=datetime.strptime(st.session_state.sleep_data.get(f"{yesterday}_waketime", "07:00"), "%H:%M").time())
        
        sleep_quality = st.select_slider("Qualité du sommeil", 
                                        options=["Très mauvaise", "Mauvaise", "Correcte", "Bonne", "Excellente"],
                                        value=st.session_state.sleep_data.get(f"{yesterday}_quality", "Bonne"))
        
        if st.button("💾 Sauvegarder sommeil"):
            st.session_state.sleep_data[f"{yesterday}_bedtime"] = sleep_time.strftime("%H:%M")
            st.session_state.sleep_data[f"{yesterday}_waketime"] = wake_time.strftime("%H:%M")
            st.session_state.sleep_data[f"{yesterday}_quality"] = sleep_quality
            save_data(st.session_state.sleep_data, 'sleep_data.json')
            st.success("Données de sommeil sauvegardées !")
    
    with col2:
        st.subheader("📊 Analyse")
        
        # Calcul durée de sommeil
        if sleep_time and wake_time:
            sleep_datetime = datetime.combine(date.today(), sleep_time)
            wake_datetime = datetime.combine(date.today() + timedelta(days=1), wake_time)
            
            if wake_time < sleep_time:  # Réveil le lendemain
                sleep_duration = wake_datetime - sleep_datetime
            else:  # Même journée
                wake_datetime = datetime.combine(date.today(), wake_time)
                sleep_duration = wake_datetime - sleep_datetime
            
            hours = sleep_duration.total_seconds() / 3600
            st.metric("Durée de sommeil", f"{hours:.1f}h")
            
            if hours >= 7 and hours <= 9:
                st.success("✅ Durée de sommeil optimale !")
            elif hours < 7:
                st.warning("⚠️ Sommeil insuffisant pour la récupération")
            else:
                st.info("💤 Peut-être un peu trop de sommeil")
        
        st.subheader("💡 Conseils sommeil")
        st.markdown("""
        • 🎯 Vise 7-9h de sommeil par nuit
        • 📱 Évite les écrans 1h avant le coucher
        • 🌡️ Garde ta chambre fraîche (18-20°C)
        • ☕ Évite la caféine après 14h
        • 🧘‍♂️ Pratique la relaxation avant de dormir
        • ⏰ Garde des horaires réguliers
        """)

# Sidebar avec informations additionnelles
with st.sidebar:
    st.markdown("### 🏆 Objectif")
    st.markdown("**Ironman 70.3**")
    st.markdown(f"📅 **24 août 2024**")
    st.markdown(f"⏱️ **Dans {days_remaining} jours**")
    
    st.markdown("### 📈 Progression")
    if total_workouts > 0:
        progress_pct = (completed_count / total_workouts) * 100
        st.progress(progress_pct / 100)
        st.markdown(f"**{progress_pct:.1f}%** des entraînements terminés")
    
    st.markdown("### 🎯 Conseils généraux")
    st.markdown("""
    • **Récupération** : Utilise étirements, rouleaux en mousse
    • **Écoute ton corps** : Ajuste si fatigue/douleurs
    • **Régularité** : Respecte le programme
    • **Hydratation** : Constante pendant l'effort
    • **Nutrition** : Équilibre à chaque repas
    """)
    
    st.markdown("### 🔄 Données")
    if st.button("🗑️ Réinitialiser toutes les données"):
        st.session_state.completed_workouts = {}
        st.session_state.sleep_data = {}
        st.session_state.nutrition_log = {}
        save_data({}, 'completed_workouts.json')
        save_data({}, 'sleep_data.json')
        save_data({}, 'nutrition_log.json')
        st.success("Données réinitialisées !")
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("💪 **Bon entraînement !** N'oublie pas : la régularité et la récupération sont clés pour réussir ton Ironman 70.3 !")