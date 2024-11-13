# Promotion des pétitions wallonnes

Compte mastodon : https://mastodon.social/@PetitionsWallonnes

Ce dépot contient un script afin de mettre en avant les pétitions wallonnes.

Pour l'instant le script permet de générer des posts pour Mastodon (https://mastodon.social/). Chaque post présente une pétition wallonne.


## Wallonie et participation citoyenne

La Constitution belge permet aux citoyens de s'exprimer et d'alerter les autorités sur leurs préoccupations. Ce droit peut s'exprimer par une pétition que l'auteur pourra présenter aux parlementaires wallons si elle est signée par au moins 1000 citoyens. Ce compte vous présente les nouvelles pétitions qui sont postées sur le site du Parlement wallon ( https://www.parlement-wallonie.be/pwpages?p=petition ) et vous invite à les signer si vous êtes d'accord avec la suggestion.


## Pourquoi signer une pétition wallonne ?

Nous avons la manière d'organiser la démocratie en Belgique est dépassée
(politiciens qui sont peu représentatifs de la population, politique qui devient plus une histoire de communication que de débat, ...). A nos yeux la participation citoyenne est une bonne piste pour répondre à ce problème.

Idéalement nous aimerions la crétaion :
- de panels citoyens (tirés au sort de manière représentative de la population) qui participeront à la prise de décision,
- d'un système de votation comme en Suisse.

Actuellements, de ces outils n'existent pas. Nous avons l'impression que ces idées mettront du temps à être mises en place et qu'il faudra défendre notre demande. Ces pétitions, nous semblent, un bon moyen pour faire avancer le schmilblick. En effet, si nous rassemblons une communauté, assez grande, de citoyens votant pour toutes les pétitions pour lesquelles le citoyen n'est pas en désaccord. Dabs ce cas, il serat courant qu'une pétition (une fois le minimum de 1000 signatures atteint) soit présentée au parlement wallon.

Bref si nous sommes solidaire, nous pouvons permettre à n'importe quel citoyen
de présenter une pétition au parlement wallon. 


## Prochaines étapes

Nous envisageons d'alimenter un compte Instagram de la même manière que nous le
faison pour Mastodon.

Par la suite nous envisageons de créer une mailing list où les citoyens wallons
pourront s'inscrire pour recevoir les nouvelles pétitions wallonnes par email.


# Comment utiliser ce script ?


## Création d'un environnement virtuel

(cette étape est option mais elle est très utile : elle permet de ne pas polluer l'environnement global de python)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Commandes

```bash
python3 main.py --help # to get help
```

## Configuration du plugin 

Créer un fichier `config.py` à partir du fichier `config.py.example` et le compléter.
