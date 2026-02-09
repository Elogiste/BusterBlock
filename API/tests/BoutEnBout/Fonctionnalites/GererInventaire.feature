# language: fr

Fonctionnalité: Gestion de l’inventaire des films par magasin
  En tant qu'employé ou manager,
  Je veux associer des films à un magasin et suivre leur stock,
  Afin de gérer la disponibilité réelle des films dans chaque magasin.

  Scénario: Ajouter un film avec quantité valide
    Étant donné un employé ou manager
    Quand il ajoute un film à l'inventaire du magasin avec une quantité valide
    Alors le film est enregistré avec la bonne disponibilité

  Scénario: Modifier la quantité ou disponibilité d'un film
    Étant donné un employé ou manager
    Quand il modifie la quantité ou la disponibilité d'un film dans l'inventaire
    Alors les changements sont enregistrés et visibles dans l'inventaire

  Scénario: Ajouter un film avec des informations invalides
    Étant donné un employé ou manager
    Quand il tente d'ajouter un film avec des informations invalides
    Alors le système retourne 400 Bad Request

  Scénario: Tentative par un utilisateur non autorisé
    Étant donné un utilisateur qui n'est pas employé ou manager
    Quand il tente de gérer l'inventaire
    Alors le système retourne 403 Forbidden
