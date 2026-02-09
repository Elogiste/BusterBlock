# language: fr

Fonctionnalité: Modifier un film du catalogue
  En tant que manager
  Je veux modifier les informations d’un film
  Afin de corriger ou améliorer ses informations dans le catalogue

  Scénario: Modifier un film avec des données valides
    Étant donné un manager authentifié
    Et un film existant avec l'identifiant 1
    Lorsque je modifie le film 1 avec des données valides
    Alors le code de retour est 200

  Scénario: Modifier un film avec des données invalides
    Étant donné un manager authentifié
    Et un film existant avec l'identifiant 1
    Lorsque je modifie le film 1 avec des données invalides
    Alors le code de retour est 400
    Et le message d'erreur est "données invalides"

  Scénario: Modifier un film inexistant
    Étant donné un manager authentifié
    Et aucun film existant avec l'identifiant 999
    Lorsque je modifie le film 999 avec des données valides
    Alors le code de retour est 404

  Scénario: Modifier un film sans être manager
    Étant donné un utilisateur non manager
    Et un film existant avec l'identifiant 1
    Lorsque je tente de modifier le film 1
    Alors le code de retour est 403
