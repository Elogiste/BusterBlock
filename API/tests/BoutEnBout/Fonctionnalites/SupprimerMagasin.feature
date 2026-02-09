# language: fr
Fonctionnalité: Supprimer un magasin

  En tant que manager, je veux supprimer un magasin qui n'est plus actif
  afin de maintenir la cohérence du catalogue et éviter que des films soient associés à un magasin fermé.

  Scénario: Supprimer un magasin existant
    Étant donné un manager
    Lorsqu'il supprime un magasin existant
    Alors le magasin est retiré de la liste publique

  Scénario: Supprimer un magasin lié à un inventaire actif
    Étant donné un manager
    Lorsqu'il tente de supprimer un magasin lié à un inventaire actif
    Alors le système refuse l'opération avec le code 409

  Scénario: Supprimer un magasin sans rôle manager
    Étant donné un utilisateur qui n'est pas manager
    Lorsqu'il tente de supprimer un magasin sans rôle manager
    Alors le système refuse l'opération avec le code 403

  Scénario: Supprimer un magasin inexistant
    Étant donné un manager
    Lorsqu'il tente de supprimer un magasin inexistant
    Alors le système renvoie le code 404
