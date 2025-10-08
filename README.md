# Cahier des Charges - API Web Modulaire FastAPI

## 1. Vue d'ensemble du projet

### 1.1. Contexte et Enjeux

Développement d'une API web modulaire et extensible servant de socle technique pour futurs projets d'application. Cette solution vise à réduire le time-to-market des nouveaux projets en fournissant une base robuste, sécurisée et scalable.

### 1.2. Objectifs Stratégiques

- **Réutilisabilité** : Créer un framework permettant de démarrer rapidement de nouveaux projets
- **Maintenabilité** : Code modulaire, documenté et testé
- **Évolutivité** : Architecture permettant l'ajout facile de nouvelles fonctionnalités
- **Performance** : API rapide et optimisée pour la production

### 1.3. Livrables Attendus

- Code source de l'API avec documentation technique complète
- Documentation utilisateur (endpoints, authentification, exemples)
- Suite de tests automatisés avec couverture > 80%
- Configuration Docker et docker-compose
- Guide de déploiement et bonnes pratiques

## 2. Exigences Fonctionnelles

### 2.1. Gestion des Utilisateurs

#### 2.1.1. Authentification

- **Inscription** : Endpoint `/auth/register` avec validation email
- **Connexion** : Endpoint `/auth/login` avec génération JWT
- **Déconnexion** : Endpoint `/auth/logout` avec révocation token
- **Récupération mot de passe** : Mécanisme de reset par email

#### 2.1.2. Gestion des Profils

- CRUD complet sur les profils utilisateurs
- Upload et gestion d'avatars (local+ fallback généré)
- Validation des données utilisateur (email unique, mot de passe fort)

#### 2.1.3. Système de Rôles

- **Rôles prédéfinis** : `user`, `admin`, `super-admin`
- **Permissions granulaires** : Attribution par ressource et opération
- **Middleware d'autorisation** : Vérification automatique des droits

### 2.2. CRUD Dynamique avec Configuration Avancée

#### 2.2.1. Configuration des Endpoints par Modèle

Chaque modèle dispose d'un système de configuration permettant de définir :

- **Endpoints disponibles** : Activation/désactivation sélective des opérations CRUD
- **Authentification par opération** : Configuration granulaire des permissions
- **Filtres d'accès** : Règles personnalisées pour l'accès aux enregistrements
- **Rate limiting** : Limitation du nombre de requêtes par endpoint

#### 2.2.2. Système d'Authentification Multi-niveaux

- **`public`** : Accès libre sans authentification
- **`users`** : Accès réservé aux utilisateurs connectés
- **`user`** : Accès limité à l'utilisateur propriétaire de l'enregistrement
- **`custom`** : Fonction personnalisée de vérification d'accès

#### 2.2.3. Contrôle d'Accès Granulaire

- **Ownership** : Définition du propriétaire d'un enregistrement via `owner_id`
- **Permissions personnalisées** : Fonctions de vérification d'accès spécifiques
- **Héritage de permissions** : Système de délégation d'accès (équipe, hiérarchie)
- **Audit des accès** : Traçabilité des consultations et modifications

#### 2.2.4. Configuration par Dictionnaire

- **Support multi-format** : Configuration via dictionnaires Python
- **Parsing automatique** : Conversion automatique des dictionnaires en objets de configuration
- **Templates prédéfinis** : Configurations type pour cas d'usage courants
- **Validation automatique** : Vérification de la cohérence des configurations

#### 2.2.5. Génération Automatique d'API

- Création automatique d'endpoints REST basée sur la configuration
- Support des opérations : `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- Pagination automatique avec paramètres configurables
- Filtrage et tri dynamiques selon les permissions

#### 2.2.6. Validation et Sérialisation

- Validation automatique via schémas Pydantic
- Sérialisation sécurisée (exclusion champs sensibles selon le niveau d'accès)
- Gestion des relations entre modèles avec permissions en cascade

### 2.3. Dashboard Administrateur (API)

#### 2.3.1. Métriques et Statistiques

- Endpoints de comptage d'entités : `/admin/stats/{model}`
- Statistiques d'utilisation : connexions, créations, etc.
- Monitoring des performances API
- Gestions des utilisateurs qui ont accès aux statistiques via la configuration

#### 2.3.2. Gestion des Données

- Endpoints de gestion en masse : import/export
- Recherche avancée multi-critères
- Historique et audit des modifications

### 2.4. Gestion des Fichiers

#### 2.4.1. Upload d'Images

- Support multi-provider : local 
- Redimensionnement et optimisation automatiques
- Génération d'avatars de fallback (initiales + couleur favorite de l'utilisateur)

#### 2.4.2. Sécurité des Fichiers

- Validation des types MIME
- Limitation de taille configurable
- Scanning antivirus

## 3. Exigences Non-Fonctionnelles

### 3.1. Performance

- **Temps de réponse** : < 200ms pour 95% des requêtes simples
- **Débit** : Support de 1000+ requêtes/seconde
- **Optimisations** : Index MongoDB
- **Pagination efficace** : Cursor-based pour gros volumes

### 3.2. Sécurité

#### 3.2.1. Authentification et Autorisation

- JWT avec rotation et expiration configurables
- Blacklist des tokens révoqués
- Protection contre le brute force (rate limiting)
- Validation stricte des entrées utilisateur

#### 3.2.2. Protection des Données

- Chiffrement des mots de passe via bcrypt
- Exposition uniquement des `public_id`
- Logs d'audit des actions sensibles
- Protection CORS configurée

### 3.3. Fiabilité

- **Disponibilité** : 99.9% en production
- **Tests automatisés** : Couverture > 80%
- **Monitoring** : Health checks et métriques
- **Gestion d'erreurs** : Codes de retour standardisés

### 3.4. Maintenabilité

- Code documenté et commenté
- Architecture modulaire et découplée
- Respect des principes SOLID
- Logging structuré et centralisé

## 4. Architecture Technique

### 4.1. Stack Technologique

#### 4.1.1. Backend

- **Framework** : FastAPI 
- **Langage** : Python 3.13
- **ORM** : ODMantic
- **Base de données** : MongoDB

#### 4.1.2. Sécurité et Validation

- **JWT** : PyJWT avec RSA256
- **Validation** : Pydantic v2
- **Hachage** : passlib avec bcrypt
- **Rate limiting** : slowapi

#### 4.1.3. Tests et Qualité

- **Tests** : pytest + httpx + mongomock
- **Couverture** : pytest-cov
- **Linting** : ruff + black
- **Type checking** : mypy

### 4.2. Architecture des Données

#### 4.2.1. BaseModel MongoDB avec Ownership

Le modèle de base comprend les champs essentiels pour la traçabilité et la propriété :

- `internal_id` : ID interne MongoDB (ObjectId)
- `public_id` : ID exposé publiquement (UUID)
- `created_at` / `updated_at` : Horodatage automatique
- `is_active` : Soft delete
- `created_by` : Utilisateur créateur
- `owner_id` : Propriétaire de l'enregistrement

#### 4.2.2. Système de Configuration des Modèles

**Classes de Configuration** :

- `AuthLevel` : Énumération des niveaux d'authentification (public, users, user, custom)
- `EndpointConfig` : Configuration d'un endpoint spécifique (auth, rate limit, filtres)
- `ModelConfig` : Configuration complète d'un modèle CRUD

**ConfigParser** :

- Convertit les dictionnaires en objets de configuration
- Maintient un registre des fonctions d'authentification personnalisées
- Valide la cohérence des configurations

**ConfigLoader** :

- Charge les configurations depuis dictionnaires Python
- Support du chargement par dossier (scan automatique)
- Gestion des templates de configuration prédéfinis

#### 4.2.3. Système de Permissions Avancé

**Interface PermissionChecker** :

- Protocole pour les vérificateurs de permissions personnalisés
- Méthode `can_access(user, record, operation)` standardisée

**Exemples de Permissions** :

- `TeamBasedPermission` : Accès basé sur l'équipe
- `HierarchicalPermission` : Accès hiérarchique (manager/équipe)
- `SharedDocumentPermission` : Documents avec partage conditionnel

#### 4.2.4. Schémas Pydantic Dynamiques

- Séparation claire : `Create`, `Update`, `Response`, `List`
- Validation métier dans les schémas
- Sérialisation conditionnelle selon les permissions
- Schémas dynamiques basés sur la configuration du modèle

### 4.3. Structure du Projet

```
myapi/
├── app/
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── config/
│   │   ├── settings.py          # Configuration par environnement
│   │   ├── database.py          # Configuration MongoDB
│   │   ├── models_config.py     # Configuration des modèles CRUD
│   │   ├── loader.py            # ConfigLoader pour dictionnaires
│   │   └── validator.py         # Validation des configurations
│   ├── core/
│   │   ├── security.py          # JWT, authentification
│   │   ├── permissions.py       # Système de permissions avancé
│   │   ├── auth_levels.py       # Niveaux d'authentification
│   │   ├── exceptions.py        # Exceptions personnalisées
│   │   ├── deps.py             # Dépendances FastAPI
│   │   └── logging.py          # Configuration des logs
│   ├── db/
│   │   ├── base.py             # BaseModel MongoDB avec ownership
│   │   └── session.py          # Gestion des sessions DB
│   ├── models/
│   │   ├── base.py             # Modèle de base avec ownership
│   │   ├── user.py             # Modèle utilisateur
│   │   ├── config.py           # Classes de configuration
│   │   ├── parser.py           # ConfigParser pour conversion dict->objets
│   │   └── registry.py         # Registre des modèles avec config
│   ├── schemas/
│   │   ├── base.py             # Schémas de base
│   │   ├── user.py             # Schémas utilisateur
│   │   ├── config.py           # Schémas de configuration
│   │   └── common.py           # Schémas communs
│   ├── api/
│   │   ├── deps.py             # Dépendances API avec auth checker
│   │   └── routes/
│   │       ├── auth.py         # Authentification
│   │       ├── users.py        # Gestion utilisateurs
│   │       ├── admin.py        # Dashboard admin
│   │       ├── files.py        # Gestion fichiers
│   │       └── dynamic.py      # CRUD dynamique configuré
│   ├── services/
│   │   ├── auth.py             # Services authentification
│   │   ├── user.py             # Services utilisateur
│   │   ├── permissions.py      # Services de permissions
│   │   ├── ownership.py        # Services de propriété
│   │   ├── file.py             # Services fichiers
│   │   └── email.py            # Services email
│   └── utils/
│       ├── validators.py       # Validateurs personnalisés
│       ├── formatters.py       # Formatage des données
│       ├── auth_decorators.py  # Décorateurs d'authentification
│       └── helpers.py          # Fonctions utilitaires
├── setup/ # Scripts d'installation et configuration 
│ ├── __init__.py 
│ ├── install.py # Script d'installation automatique 
│ ├── database_setup.py # Initialisation base de données 
│ ├── admin_setup.py # Création admin par défaut 
│ ├── config_generator.py # Générateur de configurations 
│ ├── migration.py # Scripts de migration DB
│ ├── sample_data.py # Données d'exemple pour tests
│ ├── requirements_check.py # Vérification des dépendances 
└── templates/ # Templates de configuration 
│       ├── basic_blog.json # Config blog simple 
│       ├── private_docs.yaml # Config documents privés
│       ├── team_project.json # Config projet d'équipe 
│       └── ecommerce.yaml # Config e-commerce
├── config/                     # Fichiers de configuration externes
│   ├── models.json            # Configuration JSON des modèles
│   ├── models.yaml            # Configuration YAML des modèles
│   └── models/                # Configurations séparées par modèle
├── tests/                     # Tests automatisés
├── docs/                      # Documentation
├── scripts/                   # Scripts utilitaires
└── docker/                    # Configuration Docker
```

## 5. Spécifications Détaillées

### 5.1. Endpoints Principaux

#### 5.1.1. Authentification

- `POST /auth/register` - Inscription utilisateur
- `POST /auth/login` - Connexion
- `POST /auth/logout` - Déconnexion
- `POST /auth/refresh` - Renouvellement token
- `POST /auth/forgot-password` - Demande reset mot de passe
- `POST /auth/reset-password` - Reset mot de passe

#### 5.1.2. Utilisateurs

- `GET /users/me` - Profil utilisateur loggé 
- `PUT /users/me` - Modification profil
- `POST /users/me/avatar` - Upload avatar
- `GET /users/{public_id}` - Profil utilisateur public

#### 5.1.3. Administration

- `GET /admin/stats` - Statistiques générales
- `GET /admin/users` - Liste utilisateurs (admin)
- `PUT /admin/users/{public_id}/role` - Modification rôle
- `GET /admin/logs` - Logs d'audit

#### 5.1.4. CRUD Dynamique Configuré

Les endpoints sont générés automatiquement selon la configuration de chaque modèle :

**Structure des endpoints :**

- `GET /api/{model}` - Liste des entités (selon config get_all)
- `POST /api/{model}` - Création entité (selon config create)
- `GET /api/{model}/{public_id}` - Détail entité (selon config get_one)
- `PUT /api/{model}/{public_id}` - Modification entité (selon config update)
- `DELETE /api/{model}/{public_id}` - Suppression entité (selon config delete)

**Authentification par endpoint :**

- **Public** : Accès libre, pas d'authentification requise
- **Users** : Token JWT valide requis
- **User** : Token JWT + vérification de propriété (owner_id)
- **Custom** : Fonction personnalisée de vérification d'accès

### 5.2. Système de Permissions Avancé

#### 5.2.1. Niveaux d'Authentification

|Niveau|Description|Vérification|
|---|---|---|
|`public`|Accès libre|Aucune authentification|
|`users`|Utilisateurs connectés|Token JWT valide|
|`user`|Propriétaire uniquement|JWT + ownership check|
|`custom`|Fonction personnalisée|JWT + fonction custom|

#### 5.2.2. Matrice des Rôles et Ownership

|Ressource|Public|Users|User (Owner)|Custom|
|---|---|---|---|---|
|Articles|R|CRUD|CRUD (own)|-|
|Documents privés|-|C|CRUD (own)|-|
|Projets équipe|-|R|CRUD (own)|Team-based|
|Configuration|-|-|-|Admin only|

#### 5.2.3. Système d'Ownership

**Détection automatique du propriétaire :**

- Champ `owner_id` dans le BaseModel
- Attribution automatique lors de la création (current_user.internal_id)
- Vérification lors des opérations UPDATE/DELETE

**Permissions personnalisées configurables :**

- Accès basé sur l'équipe (même team_id)
- Accès hiérarchique (manager peut accéder aux données de son équipe)
- Accès conditionnel (document partagé avec liste d'utilisateurs)
- Permissions départementales ou organisationnelles

#### 5.2.4. Configuration des Champs Sensibles

- **`owner_only_fields`** : Champs visibles uniquement par le propriétaire
- **`admin_only_fields`** : Champs visibles uniquement par les administrateurs
- **Filtrage automatique** : Exclusion des champs selon le niveau d'accès de l'utilisateur

### 5.3. Configuration par Dictionnaire

#### 5.3.1. Structure des Configurations

**Format de configuration standardisé :**

```
Configuration de modèle = {
    "model_name": string,
    "table_name": string (optionnel),
    "description": string (optionnel),
    "endpoints": {
        "get_one": EndpointConfig,
        "get_all": EndpointConfig,
        "create": EndpointConfig,
        "update": EndpointConfig,
        "delete": EndpointConfig
    },
    "ownership": {
        "owner_field": string,
        "allow_ownership_transfer": boolean,
        "ownership_check": string (nom de fonction),
        "inheritance_rules": object
    },
    "permissions": {
        "owner_only_fields": array,
        "admin_only_fields": array,
        "public_fields": array
    },
    "display": {
        "default_sort": string,
        "default_limit": integer,
        "max_limit": integer
    }
}

EndpointConfig = {
    "enabled": boolean,
    "auth_level": "public" | "users" | "user" | "custom",
    "custom_auth_func": string (nom de fonction),
    "fields_filter": object (filtres MongoDB)
}
```

#### 5.3.2. Templates Prédéfinis

**Templates pour cas d'usage courants :**

- `public_read_user_write` : Blog, articles publics
- `private_content` : Documents privés
- `team_collaboration` : Projets d'équipe avec permissions hiérarchiques

#### 5.3.3. Sources de Configuration

- **Dictionnaires Python** : Configuration par code

### 5.4. Variables d'Environnement

```
# Base de données
MONGODB_URL=mongodb://localhost:27017/myapi
REDIS_URL=redis://localhost:6379/0

# Sécurité et permissions
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Configuration CRUD dynamique
ENABLE_DYNAMIC_CRUD=true
DEFAULT_AUTH_LEVEL=users
ENABLE_OWNERSHIP_CHECK=true
DEFAULT_PAGINATION_LIMIT=20
MAX_PAGINATION_LIMIT=100

# Rate limiting
ENABLE_RATE_LIMITING=true
DEFAULT_RATE_LIMIT=100/hour
AUTH_RATE_LIMIT=5/minute

# Upload fichiers
MAX_FILE_SIZE=5242880  # 5MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-password

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn
```

## 6. Tests et Qualité

### 6.1. Stratégie de Tests

#### 6.1.1. Types de Tests

- **Tests unitaires** : Logique métier, services, parsing des configurations
- **Tests d'intégration** : API endpoints, base de données, système de permissions
- **Tests de sécurité** : Authentification, autorisations, ownership
- **Tests de configuration** : Validation des dictionnaires, parsing automatique

#### 6.1.2. Couverture Minimale

- Code coverage : > 80%
- Tests critiques : 100% (authentification, sécurité, ownership)
- Tests de configuration : Validation de tous les formats supportés

### 6.2. Outils de Qualité

- **CI/CD** : GitHub Actions avec tests automatisés
- **Analyse statique** : SonarQube
- **Monitoring** : Sentry pour les erreurs en production

## 7. Déploiement et Production

### 7.1. Containerisation

#### 7.1.1. Docker

- Image multi-stage pour optimisation
- Health checks intégrés
- Variables d'environnement sécurisées
- Support des fichiers de configuration externes

#### 7.1.2. Orchestration

- Support Kubernetes avec Helm charts
- Configuration pour différents environnements
- Auto-scaling basé sur la charge
- Configuration des volumes pour les fichiers de config

### 7.2. Monitoring et Observabilité

#### 7.2.1. Métriques

- Temps de réponse API par endpoint généré
- Taux d'erreur par endpoint et par niveau d'auth
- Utilisation des ressources
- Métriques de permissions (tentatives d'accès refusées)

#### 7.2.2. Logs

- Logs structurés (JSON)
- Corrélation des requêtes (trace ID)
- Logs d'audit des accès aux données sensibles
- Centralisation via ELK Stack ou équivalent

## 8. Sécurité

### 8.1. Mesures de Sécurité Spécifiques au CRUD Dynamique

#### 8.1.1. Authentification et Ownership

- JWT avec expiration courte et refresh token
- Vérification automatique de l'ownership sur toutes les opérations
- Rate limiting configuré par endpoint et par utilisateur
- Protection contre l'escalade de privilèges

#### 8.1.2. Protection des Données

- Validation stricte des configurations
- Exclusion automatique des champs sensibles selon les permissions
- Audit trail complet des accès aux données
- Chiffrement des données sensibles

### 8.2. Validation des Configurations

- **ConfigValidator** : Vérification de la cohérence des configurations
- **Détection des vulnérabilités** : Auth levels incohérents, fonctions manquantes
- **Sandbox des fonctions custom** : Isolation des fonctions de permissions personnalisées

## 9. Documentation

### 9.1. Documentation Technique

- Architecture du système de configuration
- Guide de création de nouvelles permissions
- Processus de déploiement avec configurations
- Troubleshooting et FAQ

### 9.2. Documentation Utilisateur

- Guide de configuration des modèles
- Référence des templates disponibles
- Exemples de configurations complexes
- Migration depuis configurations objets vers dictionnaires

## 10. Évolutions Futures

### 10.1. Roadmap Technique

- Interface graphique pour la configuration des modèles
- Support GraphQL avec permissions héritées
- Websockets temps réel avec authentification

### 10.2. Extensibilité du Système de Configuration

- Plugin system pour nouveaux types d'authentification
- Configuration via base de données
- Interface d'administration web pour les configurations
- Support de configurations conditionnelles (environnement, feature flags)

## 11. Critères d'Acceptation

### 11.1. Fonctionnels

- [ ] Système d'authentification JWT complet
- [ ] CRUD dynamique avec configuration par modèle
- [ ] Système de permissions multi-niveaux (public, users, user, custom)
- [ ] Système d'ownership et vérification d'accès
- [ ] Permissions personnalisées configurables
- [ ] **Configuration par dictionnaire/JSON/YAML**
- [ ] **Parsing automatique des configurations**
- [ ] **Templates de configuration pour cas courants**
- [ ] **Validation des configurations**
- [ ] Upload et gestion de fichiers
- [ ] Dashboard administrateur
- [ ] Rate limiting configurable par endpoint

### 11.2. Non-Fonctionnels

- [ ] Tests automatisés > 80% couverture
- [ ] Documentation complète et à jour
- [ ] Performance < 200ms (95e percentile)
- [ ] Sécurité validée par audit
- [ ] Déploiement Docker fonctionnel
- [ ] **Validation de toutes les sources de configuration**

### 11.3. Livrables

- [ ] Code source dans repository Git
- [ ] Documentation technique et utilisateur
- [ ] **Exemples de configurations pour différents cas d'usage**
- [ ] Configuration CI/CD
- [ ] Scripts de déploiement
- [ ] Guide de maintenance et de configuration

## 12. Exemples d'Utilisation du Système de Configuration

### 12.1. Configuration Blog Public


```
Configuration permettant :
- Lecture publique des articles publiés
- Création par utilisateurs connectés
- Modification/suppression par l'auteur uniquement
- Champs privés (brouillons) visibles par l'auteur seul
- Rate limiting sur la création d'articles
```

### 12.2. Configuration Documents Privés avec Partage

```
Configuration permettant :
- Accès aux documents basé sur la propriété
- Partage conditionnel via liste d'utilisateurs autorisés
- Fonction personnalisée de vérification d'accès
- Transfert de propriété possible
```

### 12.3. Configuration Projets d'Équipe


```
Configuration permettant :
- Accès basé sur l'appartenance à l'équipe
- Permissions hiérarchiques (manager peut modifier)
- Suppression restreinte aux managers
- Champs budgétaires visibles par admins uniquement
```

### 12.4. Utilisation des Templates

**Configuration rapide avec templates prédéfinis :**

```
Utilisation de templates existants avec surcharge :
- Template "public_read_user_write" pour blogs
- Template "private_content" pour documents personnels
- Template "team_collaboration" pour projets d'équipe
- Personnalisation via paramètres supplémentaires
```

---

_Ce cahier des charges définit un système complet et flexible de génération automatique d'API CRUD avec un système de configuration par dictionnaire permettant une maintenance et une extensibilité optimales._