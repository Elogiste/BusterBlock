## API de Location de Médias (BusterBlock)

## Description
Cette API REST a pour objectif de résoudre la complexité opérationnelle d'un service de location de médias pour la succursale fictive de **BusterBlock**. Elle permet de gérer de manière centralisée et automatisée le catalogue (films et jeux vidéo), les transactions de location, et les différents types d'utilisateurs. L'objectif est d'assurer une gestion plus efficace et d'optimiser l'expérience utilisateur.

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "personne non-membre" as nonMember

rectangle "API publique de BusterBlock" {
  nonMember --> (Consulter le répertoire des médias)
  nonMember --> (Rechercher un item par titre)
  nonMember --> (Consulter le détail d'un item)
  nonMember --> (Inscription au service)
  nonMember  --> (Consulter un magasin)
  nonMember  --> (Rechercher un magasin)
  nonMember  --> (Filtrer la recherche d'un magasin)
}
@enduml

```

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Membre" as member

rectangle "Accès Membre (BusterBlock API)" {
  member --> (Consulter le répertoire des médias)
  member --> (Rechercher des items)
  member --> (Location des items)
  member --> (Retour des items)
  member --> (Ré-inscription / Gestion Abonnement)
  member  --> (Consulter un magasin)
  member  --> (Rechercher un magasin)
  member  --> (Filtrer la recherche d'un magasin)
}

@enduml
```

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Employé" as employee

rectangle "Accès Employé (BusterBlock API)" {
  employee --> (Consulter le répertoire des médias)
  employee --> (Rechercher des items)
  employee --> (Modifier la location / disponibilité)
  employee --> (Consulter un magasin)
  employee --> (Rechercher un magasin)
  employee --> (Filtrer la recherche d'un magasin)
  employee --> (Gérer l’inventaire par magasin)
}
@enduml

```

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Manager" as manager

rectangle "Accès Manager (BusterBlock API)" {
  manager --> (Consulter le répertoire des médias)
  manager --> (Rechercher des items)
  manager --> (Location des items)
  manager --> (Retour des items)
  manager --> (Modifier la location / disponibilité)
  manager --> (Modifier/Ajouter/Supprimer l’item)
  manager --> (Manipuler les abonnements)
  manager  --> (Consulter un magasin)
  manager  --> (Rechercher un magasin)
  manager  --> (Filtrer la recherche d'un magasin)
  manager  --> (Gérer l’inventaire par magasin)
  manager  --> (Ajouter un magasin)
  manager  --> (Modifier un magasin)
  manager  --> (Supprimer un magasin)
}
@enduml

```

## Installation
Étapes à suivre pour installer l'API sur un serveur.

1. Clone le projet
<br>
2. Au même niveau que les fichiers Docker, ajouter le fichier .env contenant:
<br>
MARIADB_HOST=nom de votre service qui crée le conteneur de la bd, dans mon cas db
<br>
MARIADB_ROOT_PASSWORD=mot de passe de l'utilisateur root
<br>
MARIADB_DATABASE=nom de votre bd, dans mon cas busterblock_db
<br>
MARIADB_USER=nom de l'utilisateur, dans ce cas api
<br>
MARIADB_PASSWORD=mot de passe de l'utilisateur, dans ce cas root
<br>
MARIADB_PORT=3306
<br>
DOMAINE=domaine du service d'authentification, dans mon cas api_auth:8090/auth/
<br>
CLE_PUBLIQUE=adresse du point d'accès sur le serveur d'authentification pour récupérer la clé publique, dans mon cas http://api_auth:8080/auth/.well-known/jwks.json
<br>
AUDIENCE=identifiant de l'API pour laquelle le service d'authentification est offert, dans mon cas busterblock_api
<br>
ISSUER=https://api_auth:8090/auth/
<br>
3. Ajouter aussi un fichier .env-test contenant:
<br>
MARIADB_HOST=nom de votre service qui crée le conteneur de la bd, dans mon cas db
<br>
MARIADB_ROOT_PASSWORD=mot de passe de l'utilisateur root
<br>
MARIADB_DATABASE=nom de la bd de test, dans mon cas busterblock_test
<br>
MARIADB_USER=nom de l'utilisateur, dans ce cas api
<br>
MARIADB_PASSWORD=mot de passe de l'utilisateur
<br>
MARIADB_PORT=3306
<br>
4. Supprimez les conteneurs et les volumes avec la commande:
<br>
docker compose down -v
<br>
5. Recréez et relancez les conteneurs avec la commande:
<br>
docker compose up --build

## Usage

Le fonctionnement de l'API dépend des droits d'accès de l'utilisateur.

### Droits d'Accès et Authentification

Voici un aperçu des permissions par rôle :

| Acteur | Lecture du Répertoire | Inscription/Ré-inscription | Location/Retour d'Items | Modification Location/Disponibilité | CRUD sur les Médias (Item) | Manipuler Abonnements |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Non-Membre** | ✔️ | ✔️ (Inscription) | ❌ | ❌ | ❌ | ❌ |
| **Membre** | ✔️ | ✔️ (Ré-inscription) | ✔️ | ❌ | ❌ | ✔️ (Ré-inscription) |
| **Employé** | ✔️ | ❌ | ❌ | ✔️ | ❌ | ❌ |
| **Manager** | ✔️ | ❌ | ✔️ | ✔️ | ✔️ (Ajout/Modif./Suppr.) | ✔️ |

### Exemples de Requêtes (Simulation)

Voici une simulation des requêtes HTTP pour chaque rôle, utilisant le domaine fictif `https://BusterBlock/api/v1`.

#### Requêtes pour les Non-Membres

| Action | Méthode & Endpoint | Détails |
| :--- | :--- | :--- |
| **Lister tous les médias** | `GET /medias` | Retourne la liste complète du catalogue. |
| **Rechercher un média par titre** | `GET /medias?titre=Comment%Passer%Un%Projet` | Recherche filtrée par mot-clé dans le titre. |
| **Consulter le détail d'un item** | `GET /medias/420` | Retourne les informations complètes d'un média spécifique. |

#### Requêtes pour les Membres

| Action | Méthode & Endpoint | Corps (Body) |
| :--- | :--- | :--- |
| **Emprunter un item** | `POST /locations` | `{ "id_membre": 1, "id_media": 420 }` |
| **Retourner un item** | `PATCH /locations/{id_location}` | `{ "date_retour": "2025-09-23" }` |

#### Requêtes pour les Gestionnaires (Employé / Manager)

| Action | Rôle | Méthode & Endpoint | Corps (Body) |
| :--- | :--- | :--- | :--- |
| **Modifier la disponibilité** | Employé/Manager | `PUT /medias/420` | `{ "disponible": false }` |
| **Ajouter un item** | Manager | `POST /medias` | `{ "titre": "Nouveau Film", "type_media": "film", "genre": "Horreur", "disponible": true }` |
| **Supprimer un item** | Manager | `DELETE /medias/420` | |

---

## Contributeurs

### Collection de Films (Matthew)

```plantuml
@startuml
left to right direction
 
' Liste des Acteurs
rectangle "<img:https://cdn-icons-png.flaticon.com/512/3736/3736511.png{scale=0.25}>\nNon-Membre" as nm
rectangle "<img:https://cdn-icons-png.flaticon.com/512/3736/3736531.png{scale=0.25}>\nMembre" as m
rectangle "<img:https://cdn-icons-png.flaticon.com/128/3736/3736509.png{scale=1}>\nEmployé" as e 
 
' Liste des Cas d'Usages et des Méthodes
rectangle "Collections des Films" {
usecase "Consulter le Répertoire de Films" as UC1
note right of UC1 #PaleGreen : GET
usecase "Chercher un Film" as UC2
note right of UC2 #PaleGreen : GET paramétré
usecase "Consulter les Détails d'un Film" as UC3
note right of UC3 #PaleGreen : GET par ID 
usecase "Louer un Film" as UC4
note right of UC4 #LightSkyBlue : PATCH
usecase "Retourner un Film" as UC5
note right of UC5 #LightSkyBlue : PATCH
usecase "Prolonger une Location d'un Film" as UC6
note right of UC6 #LightSkyBlue : PATCH
usecase "Ajouter un Film à l'Inventaire" as UC7
note right of UC7 #LightSalmon : POST
usecase "Modifier un Film" as UC8
note right of UC8 #Plum : PUT
usecase "Modifier la Disponibilité d'un Film" as UC9
note right of UC9 #LightSkyBlue : PATCH
usecase "Retirer un Film de l'Inventaire" as UC10
note right of UC10 #IndianRed : DELETE
} 
 
' Flèches
nm --> UC1
nm --> UC2
nm --> UC3 
 
m --> UC4
m --> UC5
m --> UC6 
 
e --> UC7
e --> UC8
e --> UC9
e --> UC10 
 
' Organisation des Cas
UC1 -right- UC2 #transparent
UC2 -right- UC3 #transparent
UC8 -right- UC9 #transparent
UC7 -right- UC10 #transparent
 
' Héritage des Acteurs
nm <|-- m
m <|-- e
@enduml

```

### Collection de Magasins (Base: Matthew | Modification: Lucas)

```plantuml
@startuml
left to right direction 

' --- Acteurs ---
rectangle "<img:https://cdn-icons-png.flaticon.com/512/3736/3736531.png{scale=0.25}>\nMembre" as m
rectangle "<img:https://cdn-icons-png.flaticon.com/128/3736/3736509.png{scale=1}>\nEmployé" as e
rectangle "<img:https://cdn-icons-png.flaticon.com/512/1995/1995574.png{scale=0.25}>\nManager" as g

' --- Cas d'utilisation ---
rectangle "Collections des Magasins" {
  usecase "Chercher un Magasin" as UC1
  note right of UC1 #PaleGreen : GET paramétré

  usecase "Consulter les Détails d'un Magasin" as UC2
  note right of UC2 #PaleGreen : GET par ID

  usecase "Modifier les Détails d'un Magasin" as UC3
  note right of UC3 #LightSkyBlue : PATCH

  usecase "Ajouter un Magasin" as UC4
  note right of UC4 #LightSalmon : POST

  usecase "Retirer un Magasin" as UC5
  note right of UC5 #IndianRed : DELETE

  usecase "Filtrer les Magasins selon la Disponibilité d’un Film" as UC6
  note right of UC6 #PaleGreen : GET filtré (par disponibilité)

  usecase "Gérer l’Inventaire par Magasin" as UC7
  note right of UC7 #LightSkyBlue : PATCH / POST / DELETE selon action
}

' --- Associations ---
m --> UC1
m --> UC2
m --> UC6

e --> UC1
e --> UC2
e --> UC6
e --> UC7

g --> UC1
g --> UC2
g --> UC3
g --> UC4
g --> UC5
g --> UC6
g --> UC7

' --- Organisation visuelle ---
UC1 -right- UC3 #transparent
UC2 -right- UC3 #transparent
UC5 -right- UC4 #transparent
UC6 -down- UC2 #transparent
UC7 -right- UC5 #transparent

@enduml

```

### Diagramme de Classe (Matthew)

```plantuml
@startuml
' Config
hide circle
skinparam linetype ortho
!theme cerulean-outline

' Classes
class "**Magasins**" as Mag {
    + id : int
    --
    nom : String
    adresse : String
    telephone : String
    status : boolean
}

class "**Films**" as Fil {
    + id : int
    --
    id_magasin : int
    titre : String
    genre : String
    resume : String
    nbr_exemplaire_disponible : int
}

class "**Utilisateurs**" as Uti {
    + id : String
    --
    nom : String
    prenom : String
    courriel : String
    mot_de_passe : String
    date_creation : Timestamp
}

class "**Roles**" as Rol {
    + id : int
    --
    nom : String
}

class "**Utilisateurs_Roles**" as Uti_Rol {
    + utilisateur_id : String
    + role_id : int
}

class "**Locations**" as Loc {
    + id : int
    --
    id_utilisateur : int
    id_film : int
    id_magasin : int
    date_location : Timestamp
    date_retour : Timestamp
}

' Liens
Fil -[#Black]-> Mag

Loc -[#Black]-> Fil
Loc -[#Black]-> Mag
Loc -[#Black]-> Uti

Uti_Rol -[#Black]-> Uti
Uti_Rol -[#Black]-> Rol
@enduml

```

### Modèle Relationnel (Base: Tien | Modification: Matthew)

```plantuml
@startuml
' Config
hide circle
skinparam linetype ortho
!theme cerulean-outline
 
' Entities
entity "**Magasins**" as Mag {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> id: INT
--
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> nom: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> adresse: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> telephone: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> status: BOOLEAN
}

entity "**Films**" as Fil {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> id: INT
--
<img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> id_magasin: INT
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> titre: VARCHAR(100)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> genre: VARCHAR(50)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> resume: TEXT
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> nbr_exemplaire_disponible: INT
}

entity "**Locations**" as Loc {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> id: INT
--
<img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> id_utilisateur: INT
<img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> id_film: INT
<img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> id_magasin: INT
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> date_location: TIMESTAMP
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> date_retour: TIMESTAMP
}
 
entity "**Utilisateurs**" as Uti {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> id: VARCHAR(255)
--
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> nom: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> prenom: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> courriel: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> mot_de_passe: VARCHAR(255)
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> date_creation: TIMESTAMP
}

entity "**Roles**" as Rol {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> id: INT
--
<img:https://images.emojiterra.com/twitter/v13.1/512px/1f539.png{scale=0.035}> nom: VARCHAR(255)
}

entity "**Utilisateurs_Roles**" as Uti_Rol {
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> <img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> utilisateur_id: VARCHAR(255)
<img:https://emojis.wiki/emoji-pics/facebook/key-facebook.png{scale=0.075}> <img:https://cdn3.emoji.gg/emojis/2756_red_key.png{scale=0.0175}> role_id: INT
--
}
 
' Liens
Fil |o.[#Black].o| Mag

Uti_Rol }o.[#Black].|| Uti
Uti_Rol }o.[#Black].|| Rol
 
Loc }o.[#Black].|| Fil
Loc }o.[#Black].|| Mag
Loc }o.[#Black].|| Uti
@enduml

```

### Diagramme de Composant d'Architecture (Matthew)

```plantuml
@startuml
' Composants externes
component "Application cliente" as Client
database "Base de données" as BD

' Main Package
package "app" {

    ' Couche Interface
    package "Couche interface" {
        component "DTO" as DTO {
            [FilmBaseDTO]
            [FilmCreation]
            [FilmModification]
            [FilmRemplacement]
            [FilmReponse]

            [MagasinBaseDTO]
            [MagasinCreation]
            [MagasinModification]
            [MagasinRemplacement]
            [MagasinReponse]
        }
        component "Routeurs" as Routeurs {
            [FilmsRouteur]
            [MagasinsRouteur]
        }
        component "Securite" as Securite {
            [auth0]
            [stationsRéponse]
        }
    }

    ' Couche Métier
    package "Couche métier" {
        component "Services" as Services {
            [MagasinsService]
            [FilmsService]
        }
        component "Modele" as Modele{
            [Film]
            [Magasin]
            [MagasinBase]
        }
    }

    ' Couche d'Accès aux Données
    package "Couche d'accès aux données" {
        component "DAO" as DAO {
            [BaseDAO]
            [FilmsDAO]
            [MagasinsDAO]
        }
        component "DonneesMemoire" as DonneesMemoire {
            [donnees]
        }
    }
}

' Liens
Client --> Routeurs
Routeurs --> DTO
Securite --> Routeurs
Routeurs --> Services
Services --> Modele
Services --> DAO
DAO --> BD

@enduml

```

### Retour Item (Tien)

```plantuml
@startuml
' Actors
actor "Membre" as member
participant "Application cliente" as app
participant "API REST de BusterBlock" as api
participant "Base de données" as db

' Sequence flow
member -> app : retourne un item
app -> api : PUT /api/v1/locations/{id_location}
note right of api
  Requête pour mettre à jour
  le statut de la location.
end note

api -> db : SELECT * FROM Locations WHERE id_location = {id}
note right of db
  Vérifie que la location
  existe.
end note

db --> api : données de la location
api -> db : UPDATE Locations SET date_retour = {date_courante} WHERE id_location = {id}
note right of db
  Met à jour la date de retour.
end note

api -> db : UPDATE Medias SET disponible = TRUE WHERE id_media = {id}
note right of db
  Rend l'item à nouveau
  disponible.
end note

db --> api : confirmation
api --> app : 200 OK
app --> member : Confirmation du retour de l'item
@enduml

```

### Recherche des items (Eloge)

```plantuml
@startuml
title Rechercher des items (BusterBlock)

actor "Utilisateur (non-membre ou membre)" as user
participant "Application cliente" as client
participant "API REST BusterBlock" as api
database "BD BusterBlock" as bd

user -> client : Entrer un mot-clé et lancer la recherche
client -> api : GET /api/v1/medias?titre=motclé
api -> bd : Chercher les items correspondant au mot-clé
bd -> api : Retourner la liste d’items
api -> client : 200 OK [liste d’items JSON]
client -> user : Afficher la liste des résultats
@enduml

```

### Recherche des items sans resultats (Eloge)

```plantuml
@startuml
title Rechercher des items (aucun résultat trouvé)

actor "Utilisateur" as user
participant "Application cliente" as client
participant "API REST BusterBlock" as api
database "BD BusterBlock" as bd

user -> client : Entrer un mot-clé (ex. "FilmInexistant")
client -> api : GET /api/v1/medias?titre=FilmInexistant
api -> bd : Rechercher les items correspondant
bd -> api : Aucun item trouvé
api -> client : 200 OK []
client -> user : Afficher "Aucun résultat"
@enduml

```

### Description d'un item (Eloge)

```plantuml
@startuml
title Description d’un item (BusterBlock)

actor "Utilisateur (non-membre ou membre)" as user
participant "Application cliente" as client
participant "API REST BusterBlock" as api
database "BD BusterBlock" as bd

user -> client : Cliquer sur un item
client -> api : GET /api/v1/medias/{id}
api -> bd : Rechercher l’item par son id
bd -> api : Retourner les informations de l’item
api -> client : 200 OK {détails item JSON}
client -> user : Afficher la description complète
@enduml

```

### La répartition des tâches
Le binôme de Lucas et Eloge travaillera sur la partie Magasin de l'API.
<br>
Et celui de Matthew et Tien travaillera sur la partie Filme de l'API.

## Licence

API de locations de Medias © 2025 by Richard Tien Tran, Lucas Bidault-Meresse, Eloge Assiobo Kossi Mawuli et Matthew Sabourin est distribué sous licence CC BY-NC-SA 4.0.
Pour consulter les détails de la licence, visitez https://creativecommons.org/licenses/by-nc-sa/4.0/
