# testgen (nom provisoire)

Générateur de tests automatisés assisté par IA, avec un accent sur les tests techniques et de sécurité.

> **Statut : prototype (partie 1).** Le projet est en construction. Cette version traite une seule fonction Python à la fois.

## Pourquoi ce projet

Une part importante du code produit avec l'aide d'IA contient des failles, et les développeurs doivent tout relire pour le comprendre et le vérifier. L'objectif de ce projet est de réduire ce travail : lire du code, comprendre ce qu'il doit faire, puis générer et **vérifier** des tests adaptés.


## Principe

Le modèle de langage (LLM) ne fait pas confiance à lui-même : chaque test généré est exécuté, et seuls les résultats mesurés comptent.

1. **Extraction** : le code d'une fonction est isolé avec le module `ast` de Python (nom, signature, docstring, code source).
2. **Consigne** : on construit une consigne contenant le code, l'objectif de la fonction et les catégories de tests attendues (cas normaux, cas limites, entrées invalides, entrées malveillantes).
3. **Génération** : le LLM renvoie uniquement du code `pytest`.
4. **Exécution** : les tests sont lancés avec `pytest` dans un répertoire temporaire, avec un délai maximal.
5. **Rapport** : nombre de tests générés, réussis, échoués, en erreur, et couverture de la fonction.


## Structure du dépôt

```
testgen/
├── samples/            # fonctions témoins à tester (cibles)
├── references/         # tests écrits à la main, pour comparaison (optionnel)
├── generated/          # tests produits par l'IA (ignoré par Git)
├── src/testgen/
│   ├── __init__.py
│   ├── extract.py      # lecture du code, isolation d'une fonction
│   ├── prompt.py       # construction de la consigne
│   ├── llm.py          # appel à l'API du modèle
│   ├── runner.py       # exécution des tests générés
│   └── report.py       # affichage des résultats
├── main.py             # point d'entrée en ligne de commande
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

Prérequis : Python 3.12 ou plus récent.

```bash
git clone <adresse-du-depot>
cd testgen
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` vers `.env`, puis renseigner la clé d'API du fournisseur choisi :

```
LLM_API_KEY=votre_cle
LLM_MODEL=nom_du_modele
```

Le fichier `.env` ne doit **jamais** être envoyé sur Git (il est listé dans `.gitignore`).


## Utilisation (interface prévue)

```bash
python main.py samples/validation_ipv4.py valider_ipv4 \
    --objectif "Renvoie True si la chaîne est une adresse IPv4 valide"
```

Résultat attendu : un fichier `generated/test_valider_ipv4.py` et un rapport dans le terminal.


## Mesure de la qualité

Pour chaque fonction témoin, on note :

- les tests **valides** (compilent, passent, apportent de la couverture) ;
- les tests **inutiles** (redondants ou sans valeur) ;
- les tests **faux** (échouent à cause d'une erreur du test, pas du code).

Chaque fonction témoin contient un ou plusieurs bugs volontaires. Le prototype est considéré comme fonctionnel si au moins un test généré détecte le bug.


## Sécurité

Le code généré par un LLM est du code **non fiable**. Il est exécuté :

- dans un répertoire temporaire ;
- avec un délai maximal ;
- et, dès que possible, dans un conteneur Docker sans accès au réseau.

Ne jamais lancer les tests générés directement sur une machine contenant des données sensibles.


## Feuille de route

- [x] Partie 1 : prototype sur une fonction
- [ ] Partie 2 : boucle de correction automatique (renvoyer l'erreur au modèle)
- [ ] Partie 2 : tests de mutation pour mesurer la qualité réelle des tests
- [ ] Partie 3 : analyse d'un projet entier (graphe d'appels, dépendances)
- [ ] Partie 3 : prise en compte d'un fichier décrivant l'objectif du produit
- [ ] Partie 4 : tests de sécurité (entrées malveillantes déduites du contexte)
- [ ] Partie 4 : intégration (ligne de commande, action GitHub)


## Limites connues

- Un seul langage pris en charge (Python).
- Un test qui échoue peut signaler un vrai bug ou un test erroné : la distinction n'est pas encore automatisée.
- La qualité dépend du modèle utilisé et de la clarté de l'objectif fourni.


## Licence

À définir.