# language: fr

Fonctionnalité: Modifier la disponibilité d'un film
  En tant qu'employé
  Je veux modifier la disponibilité d'un film
  Afin de refléter l’état réel du stock

  Scénario: Modifier la disponibilité avec une valeur valide
    Étant donné un employé authentifié
    Et un film existant avec l'identifiant 1
    Lorsque je modifie la disponibilité du film 1 avec une valeur valide
    Alors le code de retour est 200

  Scénario: Modifier la disponibilité avec une valeur invalide
    Étant donné un employé authentifié
    Et un film existant avec l'identifiant 1
    Lorsque je modifie la disponibilité du film 1 avec une valeur invalide
    Alors le code de retour est 400
    Et le message d'erreur est "données invalides"

  Scénario: Modifier la disponibilité sans être employé ou manager
    Étant donné un utilisateur non employé et non manager
    Et un film existant avec l'identifiant 1
    Lorsque je tente de modifier la disponibilité du film 1
    Alors le code de retour est 403
