# language: fr

Fonctionnalité: Rechercher un film par titre
  En tant qu'utilisateur (membre ou non-membre)
  Je veux rechercher un film par son titre
  Afin de consulter ses informations dans le catalogue

  Scénario: Rechercher un film avec un titre existant
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "La guerre des étoiles"
    Alors le code de retour est 200
    Et la réponse contient au moins un film

  Scénario: Rechercher un film avec un titre inexistant
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "Titre totalement inexistant"
    Alors le code de retour est 200
    Et la liste des films retournée est vide
