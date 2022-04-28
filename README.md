Construction d’une application mobile de  **Recommandation de contenu** 👩‍🔬👨‍🔬

---
## Dossiers présents
Les éléments présents dans ce projet seront listés par la suite

**1. Data Observation **

```
Le fichier "1.Data Observaation.ipynb" contient l'analyse des données permetant la construction d'un modèle de recommandation de contenu. Il est divisé en 3 Parties :
I Observation du jeu de données
II Approche Content-Based Filtering
III Approche Collaborative Filtering
```
**2. Architecture de déploiement **
```
Le fichier "2. Architecture de déploiement.ipynb" montre des exemples de maintenance du modèle :
1. Connexion au service Microsoft Azure Blob Storage et téléchargement des fichiers dans un dossier UI/utiles
2. Création de la matrice d'entrainement
3. Ajout d'un nouvel article
4. Ajout d'un nouvel utilisateur
5. Proposition de recommandation une recommandation à un utilisateur
6. Sauvegarde du modèle et des fichiers dans le cloud d'Azure
```

** Class python --> Entretien du modèle  **

```
Le fichier "class.py" contient la class permettant d'effectuer l'entretien du modèle.
A noté que les identifiants de connexion seront désactivé à compter du 15 juin 2022.
```

** Dossier bookshelf **
```
Le dossier "bookshelf" contient les fichiers permettant de faire tourner l'application sous android via le framewoork Expo.

Le fichier "config.json" a été modifié pour introduire l'adresse URL hébergeant l'application de recommandation sur le serverless Azure Functions.

Le fichier "package.json" a également été modifié pour changer la version d'expo qui passe de 33.0 à 44.0.0 plus stable.
```


** Dossier functionOC **
```
Le dossier "functionOC" contient les fichiers permettant de faire tourner la fonction de recommandation qui s'éxécutera sur le serverless Azure Function via une requette URL.

Le fichier '__init__.py' a été modifié afin de pouvoir importer le model de prédiction développé via la bibliothèque implicit, (la bibliothèque suprise a également été testé mais ne figure plus dans les fichiers de ce projet --> 1.Data Observaation.ipynb).

Dans l'architecture fonctionnelle de l'application, le modèle doit être importé depuis l'espace de stockage Azure Blob Storage, cette fonctionnalité a été retiré afin d'améliorer l'activiation du service.

Enfin le fichier sparse.npz est la matrice article/score/utilisateur qui permet au modèle de faire des prédiction.


```
** Dossier Github **
```
https://github.com/Mickevin/Application-mobile-de-recommandation-de-contenu

```
