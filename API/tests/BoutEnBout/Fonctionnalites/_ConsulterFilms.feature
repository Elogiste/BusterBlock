# language: fr

Fonctionnalité: Consultation et recherche de films
  En tant qu'utilisateur de BusterBlock
  Je veux consulter et rechercher des films
  Afin de connaître leurs détails et leur disponibilité dans un magasin

  Scénario: Consulter le détail d’un film existant
    Étant donné un film existant avec l'identifiant 1
    Lorsque je consulte les détails du film 1
    Alors le code de retour est 200
    Et la réponse contient les informations détaillées du film

  Scénario: Consulter le détail d’un film inexistant
    Étant donné aucun film existant avec l'identifiant 999
    Lorsque je consulte les détails du film 999
    Alors le code de retour est 404
    Et le message d'erreur est "film avec id 999 non trouvé."

  Scénario: Consulter la disponibilité d’un film dans un magasin où il est disponible
    Étant donné un film existant avec l'identifiant 1 disponible dans le magasin 101
    Lorsque je consulte les détails du film 1 pour le magasin 101
    Alors le code de retour est 200
    Et le film est indiqué comme disponible dans ce magasin

  Scénario: Consulter la disponibilité d’un film dans un magasin où il est indisponible
    Étant donné un film existant avec l'identifiant 2 dans le magasin 101 sans exemplaire disponible
    Lorsque je consulte les détails du film 2 pour le magasin 101
    Alors le code de retour est 200
    Et le film est indiqué comme non disponible dans ce magasin

  Scénario: Rechercher un film par son titre
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "La guerre des étoiles"
    Alors le code de retour est 200
    Et la réponse contient au moins un film

  Scénario: Rechercher un film par un titre inexistant
    Étant donné des films existent dans le système
    Lorsque je recherche les films avec le titre "Titre totalement inexistant"
    Alors le code de retour est 200
    Et la liste des films retournée est vide

  Scénario: Rechercher des films par genre
    Étant donné des films existent dans le système
    Lorsque je recherche les films du genre "Science-Fiction"
    Alors le code de retour est 200
    Et la réponse contient au moins un film
    Et tous les films retournés ont le genre "Science-Fiction"
