# language: fr

Fonctionnalité: Consulter le détail d'un film
  En tant qu'utilisateur
  Je veux consulter le détail d'un film
  Afin de voir les informations essentielles et sa disponibilité

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

  Scénario: Consulter la disponibilité d’un film dans un magasin où il est indisponible
    Étant donné un film existant avec l'identifiant 2 dans le magasin 101 sans exemplaire disponible
    Lorsque je consulte les détails du film 2 pour le magasin 101
    Alors le code de retour est 200
