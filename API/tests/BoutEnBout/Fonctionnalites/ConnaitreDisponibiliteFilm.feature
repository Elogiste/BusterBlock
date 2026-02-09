# language: fr

Fonctionnalité: Connaître la disponibilité d'un film
  En tant qu'utilisateur
  Je veux chercher un film selon des paramètres
  Afin de connaître sa disponibilité dans le catalogue

  Scénario: Connaître la disponibilité d'un film par son titre
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "La guerre des étoiles"
    Alors le code de retour est 200
    Et la réponse contient au moins un film

  Scénario: Connaître la disponibilité d'un film par son genre
    Étant donné des films existent dans le système
    Lorsque je recherche les films du genre "Science-Fiction"
    Alors le code de retour est 200
    Et la réponse contient au moins un film
    Et tous les films retournés ont le genre "Science-Fiction"

  Scénario: Connaître la disponibilité d'un film lorsque aucun résultat ne correspond
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "Titre totalement inexistant"
    Alors le code de retour est 200
    Et la liste des films retournée est vide
