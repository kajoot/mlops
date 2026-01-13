# 📦 LIVRABLES - Mini-projet MLOps

**Projet:** Classification multi-classe UCI Iris  
**Modèles:** Logistic Regression + SVM (scikit-learn)  
**Date:** 13 janvier 2026

---

## ✅ LISTE DES LIVRABLES

### 1. 🔗 Lien Github/GitLab
**Statut:** ✅ READY (besoin d'ajouter remote)

**Fichiers de preuve:**
- `deliverables/1_git_history.txt` - Historique complet des commits
- `deliverables/1_git_status.txt` - État du dépôt
- `deliverables/1_git_remote.txt` - Configuration remote

**Commande pour push:**
```bash
git remote add origin <votre-url-gitlab>
git push -u origin master --tags
```

**Contenu du dépôt:**
- ✅ 6 commits avec messages clairs
- ✅ Tag v1.0
- ✅ README.md complet
- ✅ Structure de projet claire
- ✅ .gitignore approprié

---

### 2. 🐳 Dockerfiles + docker-compose.yml
**Statut:** ✅ COMPLET

**Fichiers de preuve:**
- `deliverables/2_docker-compose.yml` - Configuration multi-services
- `deliverables/2_Dockerfile.api` - Image API d'inférence
- `deliverables/2_Dockerfile.train` - Image d'entraînement
- `deliverables/2_docker_services_status.txt` - État des services

**Services Docker:**
- ✅ mlflow-server (port 5000)
- ✅ api-v1 (port 8000)
- ✅ api-v2 (port 8001, profile: v2)

**Commandes de test:**
```bash
docker-compose up -d
docker-compose ps
curl http://localhost:8000/health
```

---

### 3. 📊 Config DVC + preuve push/pull
**Statut:** ✅ COMPLET

**Fichiers de preuve:**
- `deliverables/3_dvc_remote_config.txt` - Configuration du remote
- `deliverables/3_dvc_tracked_files.txt` - Fichiers trackés
- `deliverables/3_dvc_status.txt` - État DVC

**Configuration DVC:**
- ✅ Remote: local (`./dvc_remote`)
- ✅ Fichiers trackés: `train.csv`, `test.csv`
- ✅ Push réussi: 2 files pushed
- ✅ Pull fonctionnel: Everything is up to date

**Commandes de démonstration:**
```bash
dvc remote list -v
dvc status
dvc push
dvc pull
```

---

### 4. 📈 Captures MLflow et ZenML
**Statut:** ✅ COMPLET

**Fichiers de preuve MLflow:**
- `deliverables/4_mlflow_experiments.json` - Données complètes des expériences
- URL: http://localhost:5000

**Résultats MLflow:**
- ✅ 2 expériences créées:
  - `iris-classification`: 2 runs (baseline LR + SVM)
  - `iris-classification-optimized`: 1 run (Optuna)
- ✅ Paramètres loggés: C, kernel, max_iter, model_type
- ✅ Métriques loggées: accuracy, f1_score, test_accuracy
- ✅ Artifacts: models, classification reports, confusion matrices
- ✅ Résultats:
  - Baseline: 96.67% accuracy
  - Optimized: 100% accuracy

**Fichiers de preuve ZenML:**
- `deliverables/5_zenml_pipeline_runs.txt` - Liste des exécutions
- `deliverables/5_zenml_stack.txt` - Configuration du stack

**Résultats ZenML:**
- ✅ Pipeline: `iris_training_pipeline`
- ✅ 4 exécutions totales (2 réussies, 2 échecs initiaux)
- ✅ Steps: load_data → train_model → evaluate_model → save_model
- ✅ Stack: default (orchestrator + artifact_store)

**Commandes pour captures:**
```bash
# MLflow UI
firefox http://localhost:5000

# ZenML dashboard
zenml up
firefox http://localhost:8237
```

---

### 5. ⚙️ .gitlab-ci.yml (optionnel)
**Statut:** ✅ COMPLET

**Fichiers de preuve:**
- `deliverables/6_gitlab-ci.yml` - Pipeline CI/CD complet

**Configuration CI/CD:**
- ✅ 4 stages: test, build, deploy, continuous-training
- ✅ Jobs:
  - `lint`: Validation du code avec flake8/black
  - `test`: Tests unitaires avec pytest
  - `build_train_image`: Build Docker training
  - `build_api_image`: Build Docker API
  - `deploy_v1`: Déploiement version 1
  - `deploy_v2`: Déploiement version 2
  - `continuous_training`: Entraînement automatique (schedule)

---

### 6. 🚀 Démo déploiement v1→v2→rollback
**Statut:** ✅ TESTÉ ET VALIDÉ

**Fichiers de preuve:**
- `deliverables/7_deployment_demo.txt` - Trace complète du déploiement

**Scénario testé:**
1. ✅ **Démarrage v1** (port 8000)
   - Health check: OK
   - Predictions: OK (setosa, versicolor, virginica)
   
2. ✅ **Déploiement v2** (port 8001)
   - Build image: OK
   - Démarrage container: OK
   - Les deux versions coexistent
   
3. ✅ **Test des deux versions**
   - v1 (8000): Health OK, Predictions OK
   - v2 (8001): Health OK, Predictions OK
   
4. ✅ **Rollback (stop v2)**
   - v2 arrêté proprement
   - v1 continue de servir sans interruption
   
**Commandes de démonstration:**
```bash
# Démarrer v1
docker-compose up -d

# Tester v1
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

# Déployer v2
docker-compose --profile v2 up -d api-v2

# Vérifier les deux versions
curl http://localhost:8000/health  # v1
curl http://localhost:8001/health  # v2

# Rollback
docker-compose stop api-v2

# Vérifier v1 toujours up
curl http://localhost:8000/health
```

---

### 7. 📚 Documentation README
**Statut:** ✅ COMPLET

**Fichiers de preuve:**
- `deliverables/8_README.md` - Documentation principale (8.1 KB)
- `deliverables/8_QUICKSTART.md` - Guide de démarrage rapide (4.6 KB)
- `deliverables/8_PROJECT_SUMMARY.md` - Résumé du projet (9.2 KB)

**Contenu README:**
- ✅ Description du projet
- ✅ Architecture complète
- ✅ Instructions d'installation
- ✅ Guide d'utilisation
- ✅ Détails des pipelines MLOps
- ✅ Configuration DVC/MLflow/ZenML
- ✅ Déploiement Docker
- ✅ API endpoints
- ✅ CI/CD pipeline
- ✅ Troubleshooting

---

## 📊 RÉSUMÉ DES TESTS

**Fichier de preuve:**
- `deliverables/9_test_summary.json` - Résultats complets

### Tests effectués:

| Composant | Statut | Détails |
|-----------|--------|---------|
| **Git** | ✅ PASS | 6 commits, tag v1.0, structure claire |
| **DVC** | ✅ PASS | 2 fichiers trackés, push/pull OK |
| **MLflow** | ✅ PASS | 2 expériences, 3 runs, accuracy 96.67% → 100% |
| **ZenML** | ✅ PASS | 1 pipeline, 2 runs réussis |
| **Models** | ✅ PASS | 4 modèles, 100% prédictions correctes |
| **Docker** | ✅ PASS | 3 services, déploiement/rollback OK |
| **API** | ✅ PASS | Tous endpoints fonctionnels |
| **CI/CD** | ✅ PASS | Pipeline GitLab complet |

---

## 🎯 CONTENU DU PROJET (Cahier des charges)

### 3.1 Dataset + Baseline + Métrique
- ✅ Dataset: UCI Iris (150 samples, 3 classes)
- ✅ Baseline: Logistic Regression + SVM
- ✅ Métrique: Accuracy (96.67% baseline, 100% optimized)

### 3.2 Git propre + README
- ✅ Repo initialisé avec 6 commits
- ✅ README.md complet (8.1 KB)
- ✅ Structure claire (src/, data/, models/, api/, pipelines/)
- ✅ Tag v1.0
- ✅ .gitignore approprié

### 3.3 Dockerfile(s) + docker-compose
- ✅ Dockerfile.train pour entraînement
- ✅ Dockerfile.api pour inférence
- ✅ docker-compose.yml avec 3 services
- ✅ Healthchecks configurés

### 3.4 DVC tracking + remote
- ✅ DVC initialisé
- ✅ Remote configuré (local)
- ✅ 2 datasets trackés (train.csv, test.csv)
- ✅ Push/pull fonctionnels

### 3.5 MLflow ≥1 baseline run
- ✅ 2 expériences créées
- ✅ 3 runs enregistrés
- ✅ Paramètres, métriques, artifacts loggés
- ✅ Comparaison baseline vs optimized

### 3.6 Pipeline ZenML + plusieurs exécutions
- ✅ Pipeline iris_training_pipeline créé
- ✅ 4 steps: load_data, train_model, evaluate_model, save_model
- ✅ 2 exécutions réussies (LR + SVM)

### 3.7 Optuna 5-10 trials
- ✅ 10 trials effectués
- ✅ Optimisation hyperparamètres (C, max_iter)
- ✅ Amélioration: 96.67% → 100% accuracy
- ✅ Best model loggé dans MLflow

### 3.8 GitLab CI avec tests/lint/build
- ✅ .gitlab-ci.yml créé
- ✅ 4 stages: test, build, deploy, CT
- ✅ Lint avec flake8/black
- ✅ Tests unitaires
- ✅ Build Docker images
- ✅ Continuous Training configuré

### 3.9 API d'inférence + Docker Compose v1→v2
- ✅ FastAPI avec /predict, /health, /reload
- ✅ Docker Compose multi-services
- ✅ Déploiement v1 + v2 testé
- ✅ Rollback fonctionnel

---

## 📁 STRUCTURE DES LIVRABLES

```
deliverables/
├── 1_git_history.txt              # Historique Git
├── 1_git_status.txt               # État du dépôt
├── 1_git_remote.txt               # Configuration remote
├── 2_docker-compose.yml           # Orchestration services
├── 2_Dockerfile.api               # Image API
├── 2_Dockerfile.train             # Image training
├── 2_docker_services_status.txt   # État services Docker
├── 3_dvc_remote_config.txt        # Config DVC
├── 3_dvc_tracked_files.txt        # Fichiers trackés
├── 3_dvc_status.txt               # État DVC
├── 4_mlflow_experiments.json      # Données MLflow
├── 5_zenml_pipeline_runs.txt      # Exécutions ZenML
├── 5_zenml_stack.txt              # Stack ZenML
├── 6_gitlab-ci.yml                # Pipeline CI/CD
├── 7_deployment_demo.txt          # Démo déploiement
├── 8_README.md                    # Documentation
├── 8_QUICKSTART.md                # Quick start
├── 8_PROJECT_SUMMARY.md           # Résumé
├── 9_test_summary.json            # Résultats tests
└── DELIVERABLES_CHECKLIST.md      # Ce fichier
```

---

## 🚀 COMMANDES RAPIDES POUR DÉMO

```bash
# 1. Démarrer tous les services
docker-compose up -d

# 2. Vérifier MLflow
firefox http://localhost:5000

# 3. Tester l'API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

# 4. Montrer DVC
dvc status
dvc remote list

# 5. Montrer ZenML
zenml pipeline runs list

# 6. Montrer Git
git log --oneline --graph
git tag

# 7. Déploiement v2
docker-compose --profile v2 up -d api-v2
curl http://localhost:8001/health

# 8. Rollback
docker-compose stop api-v2
curl http://localhost:8000/health  # v1 toujours up
```

---

## ✅ CHECKLIST FINALE

- [x] Tous les tests passent
- [x] Documentation complète
- [x] Code propre et commenté
- [x] Docker images buildent
- [x] Services démarrent correctement
- [x] API répond aux requêtes
- [x] DVC push/pull fonctionnent
- [x] MLflow logs les expériences
- [x] ZenML pipelines s'exécutent
- [x] Déploiement v1→v2→rollback OK
- [x] Fichiers de preuve générés
- [x] Prêt pour la présentation

---

**✅ PROJET COMPLET - PRÊT POUR SOUMISSION**
