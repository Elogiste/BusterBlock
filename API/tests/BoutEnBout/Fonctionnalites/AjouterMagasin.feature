# language: fr
Fonctionnalité: Ajouter un magasin

  En tant que manager, je veux ajouter un magasin,
  afin d'augmenter le réseau de distribution et gérer de nouveaux stocks.

  Scénario: Ajouter un magasin valide
    Étant donné un manager
    Quand il ajoute un nouveau magasin avec toutes les informations valides
    Alors le magasin est enregistré

  Scénario: Ajouter un magasin invalide
    Étant donné un manager
    Quand il ajoute un magasin avec des informations manquantes ou invalides
    Alors le système refuse la requête avec le code 422

  Scénario: Ajouter un magasin sans rôle manager
    Étant donné un utilisateur qui n'est pas manager
    Quand il tente d'ajouter un nouveau magasin
    Alors le système refuse l'opération avec le code 403
