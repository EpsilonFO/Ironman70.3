# 🏊‍♂️ Application de Préparation Ironman 70.3

Une application Streamlit complète pour suivre votre entraînement, nutrition et récupération en vue d'un Ironman 70.3.

## 🎯 Fonctionnalités

### 📅 **Programme quotidien**
- Entraînements automatiques selon votre planning
- Cases à cocher pour marquer les séances terminées
- Conseils nutritionnels personnalisés par jour

### 💪 **Suivi des entraînements**
- Programme de 3 semaines intégré (natation, vélo, course à pied)
- Vue d'ensemble par semaine
- Progression visuelle en temps réel

### 🍽️ **Gestion nutrition**
- Log quotidien des repas (petit-déjeuner, déjeuner, dîner, collations)
- Suivi d'hydratation avec objectif 3L/jour
- 8 conseils nutritionnels essentiels

### 😴 **Monitoring du sommeil**
- Enregistrement heures coucher/réveil
- Évaluation qualité du sommeil
- Analyse durée et conseils récupération

### 📊 **Tableau de bord**
- Compte à rebours jusqu'à la course
- Statistiques de progression
- Pourcentage d'entraînements réalisés

## 🚀 Installation et lancement

### Prérequis
```bash
pip install streamlit pandas
```

### Démarrage
1. Téléchargez le fichier `ironman_app.py`
2. Ouvrez un terminal dans le dossier du fichier
3. Lancez l'application :
```bash
streamlit run ironman_app.py
```
4. Ouvrez votre navigateur à l'adresse affichée (généralement `http://localhost:8501`)

## 📱 Utilisation

### Premier lancement
- L'application détecte automatiquement la semaine actuelle
- Tous vos progrès sont sauvegardés automatiquement
- Accessible depuis mobile, tablette et ordinateur

### Navigation
- **Programme du jour** : Consultez vos entraînements quotidiens
- **Entraînements** : Vue d'ensemble hebdomadaire
- **Nutrition** : Loggez vos repas et hydratation
- **Sommeil** : Suivez votre récupération

### Données sauvegardées
L'application crée automatiquement 3 fichiers de sauvegarde :
- `completed_workouts.json` : Entraînements terminés
- `sleep_data.json` : Données de sommeil
- `nutrition_log.json` : Log nutrition et hydratation

## ⚙️ Configuration

### Dates importantes
- **Début du programme** : 29 juin 2025
- **Date de course** : 24 août 2025
- **Durée** : 3 semaines d'entraînement intensif

### Personnalisation
Pour adapter le programme, modifiez la variable `TRAINING_PROGRAM` dans le code :
- Ajoutez/supprimez des séances
- Modifiez les descriptions d'entraînement
- Personnalisez les conseils nutrition

## 🔧 Fonctionnalités avancées

### Réinitialisation
Bouton "Réinitialiser toutes les données" dans la sidebar pour repartir à zéro.

### Calculs automatiques
- Détection semaine actuelle
- Progression en pourcentage
- Durée de sommeil
- Objectifs hydratation

## 🎨 Interface

- **Design responsive** : Optimisé mobile et desktop
- **Codes couleur** : Natation (rouge), Vélo (bleu), Course (vert)
- **Interface intuitive** : Cases à cocher, métriques visuelles
- **Thème moderne** : Cartes, gradients, ombres

## 📈 Suivi de progression

L'application calcule automatiquement :
- Jours restants avant la course
- Nombre total d'entraînements
- Entraînements terminés
- Pourcentage de progression

## 💡 Conseils d'utilisation

1. **Consultez quotidiennement** le programme du jour
2. **Cochez immédiatement** les entraînements terminés
3. **Loggez votre nutrition** chaque soir
4. **Enregistrez votre sommeil** chaque matin
5. **Suivez votre hydratation** tout au long de la journée

## 🏆 Objectif

Vous préparer optimalement pour réussir votre **Ironman 70.3 le 24 août 2025** !

---

*Bon entraînement ! 💪 La régularité et la récupération sont les clés du succès.*
