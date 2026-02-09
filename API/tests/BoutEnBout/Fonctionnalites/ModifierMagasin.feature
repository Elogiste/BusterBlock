# language: fr
Fonctionnalité: Modifier un magasin

  En tant que manager, je veux modifier les informations d'un magasin
  afin de corriger ou mettre à jour les données existantes.

  Scénario: Modifier un magasin avec des informations valides
    Étant donné un manager
    Quand il modifie un magasin avec des informations valides
    Alors les modifications sont enregistrées et reflétées dans la liste des magasins

  Scénario: Modifier un magasin avec des informations invalides
    Étant donné un manager
    Quand il tente de modifier un magasin avec des informations invalides
    Alors le système refuse la modification avec le code 400

  Scénario: Modifier un magasin sans rôle manager
    Étant donné un utilisateur qui n'est pas manager
    Quand il tente de modifier un magasin
    Alors le système refuse l'opération avec le code 403

  Scénario: Modifier un magasin inexistant
    Étant donné un magasin inexistant
    Quand un manager ou un employé tente de le modifier
    Alors le système renvoie le code 404
