#language: fr

Fonctionnalité: Rechercher un magasin
  En tant qu’utilisateur
  Je veux rechercher un magasin par son identifiant, son nom ou une partie de son adresse
  Afin de savoir rapidement où un film est disponible ou quel magasin est le plus proche

  Scénario: Rechercher un magasin par son identifiant
    Étant donné un magasin existant avec l'identifiant 3
    Lorsque je recherche le magasin avec l'identifiant 3
    Alors le code de retour est 200
    Et la réponse contient les informations du magasin (id, nom, adresse, téléphone, statut)

  Scénario: Rechercher un magasin par son nom
    Étant donné un magasin existant portant le nom "BusterBlock Montréal"
    Lorsque je recherche le magasin par le nom "BusterBlock Montréal"
    Alors le code de retour est 200
    Et la réponse contient les informations du magasin (id, nom, adresse, téléphone, statut)

  Scénario: Rechercher un magasin par des caractères contenus dans son adresse
    Étant donné des magasins contenant "Québec" dans leur adresse
    Lorsque je recherche un magasin contenant "Québec" dans son adresse
    Alors le code de retour est 200
    Et la réponse contient la liste des magasins correspondants avec leurs informations (id, nom, adresse, téléphone, statut)

  Scénario: Rechercher un magasin avec un critère inexistant
    Étant donné qu'aucun magasin ne correspond au critère "BusterBlock Alma"
    Lorsque je recherche un magasin avec le critère inexistant "BusterBlock Alma"
    Alors le code de retour est 200
    Et le résultat est une liste vide
    Et le message indique "Aucun magasin ne correspond à la recherche"
