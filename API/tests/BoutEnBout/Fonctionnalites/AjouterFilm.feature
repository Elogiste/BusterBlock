# language: fr

Fonctionnalité: Ajouter un nouveau film au catalogue
  En tant que manager
  Je veux ajouter un nouveau film avec toutes ses informations
  Afin d’offrir plus de films aux membres

  Scénario: Ajouter un film avec des informations valides
    Étant donné un manager authentifié
    Lorsque j'ajoute un nouveau film avec des informations valides
    Alors le code de retour est 201

  Scénario: Ajouter un film avec des informations invalides
    Étant donné un manager authentifié
    Lorsque j'ajoute un nouveau film avec des informations invalides
    Alors le code de retour est 400
    Et le message d'erreur est "données invalides"
