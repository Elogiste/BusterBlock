# language: fr

Fonctionnalité: Supprimer un film du catalogue
  En tant que manager
  Je veux supprimer un film du catalogue
  Afin de respecter les licences de BusterBlock

  Scénario: Supprimer un film existant
    Étant donné un manager authentifié
    Et un film existant avec l'identifiant 1
    Lorsque je supprime le film 1
    Alors le code de retour est 200

  Scénario: Supprimer un film inexistant
    Étant donné un manager authentifié
    Et aucun film existant avec l'identifiant 999
    Lorsque je supprime le film 999
    Alors le code de retour est 404

  Scénario: Supprimer un film sans être manager
    Étant donné un utilisateur non manager
    Et un film existant avec l'identifiant 1
    Lorsque je tente de supprimer le film 1
    Alors le code de retour est 403
